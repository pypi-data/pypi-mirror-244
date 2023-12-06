from copy import deepcopy
from typing import Tuple, Callable, Dict
from joblib import Parallel, delayed

import numpy as np

from . import Preprocessor, MatchingData
from .backends import backend
from .types import NDArray, CallbackClass
from .matching_memory import CCMemoryUsage
from .analyzer import MaxScoreOverRotations
from .matching_exhaustive import register_matching_exhaustive, device_memory_handler
from .matching_utils import apply_convolution_mode, conditional_execute

def corr2_setup(
    rfftn: Callable,
    irfftn: Callable,
    template: NDArray,
    template_mask: NDArray,
    target: NDArray,
    fast_shape: Tuple[int],
    fast_ft_shape: Tuple[int],
    real_dtype: type,
    complex_dtype: type,
    shared_memory_handler: Callable,
    callback_class: Callable,
    callback_class_args: Dict,
    **kwargs,
) -> Dict:
    """
    Setup to compute a normalized cross-correlation score of a target f a template g
    and a mask m:

    .. math::

        \\frac{CC(f, \\frac{g*m - \\overline{g*m}}{\\sigma_{g*m}})}
        {N_m * \\sqrt{
            \\frac{CC(f^2, m)}{N_m} - (\\frac{CC(f, m)}{N_m})^2}
        }

    Where:

    .. math::

        CC(f,g) = \\mathcal{F}^{-1}(\\mathcal{F}(f) \\cdot \\mathcal{F}(g)^*)

    and Nm is the number of voxels within the template mask m.

    References
    ----------
    .. [1]  W. Wan, S. Khavnekar, J. Wagner, P. Erdmann, and W. Baumeister
            Microsc. Microanal. 26, 2516 (2020)
    .. [2]  T. Hrabe, Y. Chen, S. Pfeffer, L. Kuhn Cuellar, A.-V. Mangold,
            and F. Förster, J. Struct. Biol. 178, 177 (2012).

    See Also
    --------
    :py:meth:`flc_scoring`
    """
    target_pad = backend.topleft_pad(target, fast_shape)

    # Target and squared target window sums
    ft_target = backend.preallocate_array(fast_ft_shape, complex_dtype)
    ft_target2 = backend.preallocate_array(fast_ft_shape, complex_dtype)
    rfftn(target_pad, ft_target)
    rfftn(backend.square(target_pad), ft_target2)

    # Convert arrays used in subsequent fitting to SharedMemory objects
    ft_target = backend.arr_to_sharedarr(
        arr=ft_target, shared_memory_handler=shared_memory_handler
    )
    ft_target2 = backend.arr_to_sharedarr(
        arr=ft_target2, shared_memory_handler=shared_memory_handler
    )

    template_buffer = backend.arr_to_sharedarr(
        arr=template, shared_memory_handler=shared_memory_handler
    )
    template_mask_buffer = backend.arr_to_sharedarr(
        arr=template_mask, shared_memory_handler=shared_memory_handler
    )

    template_tuple = (template_buffer, template.shape, real_dtype)
    template_mask_tuple = (template_mask_buffer, template_mask.shape, real_dtype)

    target_ft_tuple = (ft_target, fast_ft_shape, complex_dtype)
    target_ft2_tuple = (ft_target2, fast_ft_shape, complex_dtype)

    ret = {
        "template": template_tuple,
        "template_mask": template_mask_tuple,
        "ft_target": target_ft_tuple,
        "ft_target2": target_ft2_tuple,
        "targetshape": target.shape,
        "templateshape": template.shape,
        "fast_shape": fast_shape,
        "fast_ft_shape": fast_ft_shape,
        "real_dtype": real_dtype,
        "complex_dtype": complex_dtype,
        "callback_class": callback_class,
        "callback_class_args": callback_class_args,
    }

    return ret


def corr2_scoring(
    template: Tuple[type, Tuple[int], type],
    template_mask: Tuple[type, Tuple[int], type],
    ft_target: Tuple[type, Tuple[int], type],
    ft_target2: Tuple[type, Tuple[int], type],
    template_filter: Tuple[type, Tuple[int], type],
    targetshape: Tuple[int],
    templateshape: Tuple[int],
    fast_shape: Tuple[int],
    fast_ft_shape: Tuple[int],
    rotations: NDArray,
    real_dtype: type,
    complex_dtype: type,
    callback_class: CallbackClass,
    callback_class_args: Dict,
    interpolation_order: int,
    **kwargs,
) -> CallbackClass:
    template_buffer, template_shape, template_dtype = template
    template_mask_buffer, *_ = template_mask
    filter_buffer, filter_shape, filter_dtype = template_filter

    ft_target_buffer, ft_target_shape, ft_target_dtype = ft_target
    ft_target2_buffer, *_ = ft_target2

    if callback_class is not None and isinstance(callback_class, type):
        callback = callback_class(**callback_class_args)
    elif not isinstance(callback_class, type):
        callback = callback_class

    # Retrieve objects from shared memory
    template = backend.sharedarr_to_arr(template_shape, template_dtype, template_buffer)
    template_mask = backend.sharedarr_to_arr(
        template_shape, template_dtype, template_mask_buffer
    )
    ft_target = backend.sharedarr_to_arr(
        ft_target_shape, ft_target_dtype, ft_target_buffer
    )
    ft_target2 = backend.sharedarr_to_arr(
        ft_target_shape, ft_target_dtype, ft_target2_buffer
    )
    template_filter = backend.sharedarr_to_arr(
        filter_shape, filter_dtype, filter_buffer
    )

    arr = backend.preallocate_array(fast_shape, real_dtype)
    temp = backend.preallocate_array(fast_shape, real_dtype)
    temp2 = backend.preallocate_array(fast_shape, real_dtype)

    ft_temp = backend.preallocate_array(fast_ft_shape, complex_dtype)
    ft_denom = backend.preallocate_array(fast_ft_shape, complex_dtype)

    rfftn, irfftn = backend.build_fft(
        fast_shape=fast_shape,
        fast_ft_shape=fast_ft_shape,
        real_dtype=real_dtype,
        complex_dtype=complex_dtype,
        fftargs=kwargs.get("fftargs", {}),
        temp_real=arr,
        temp_fft=ft_temp,
    )

    templateshape = list(templateshape)
    templateshape[-1] = 1

    subset = [slice(0, x) for x in templateshape]
    subset.pop(-1)
    subset = tuple(subset)
    temp_shape = list(fast_shape)
    temp_shape[-1] = template.shape[-1]
    rotation_out = backend.preallocate_array(temp_shape, real_dtype)

    from time import time

    for index in range(rotations.shape[0]):
        start = time()
        rotation = rotations[index]
        backend.fill(arr, 0)
        backend.fill(temp, 0)
        backend.fill(rotation_out, 0)

        backend.rotate_array(
            arr=template,
            rotation_matrix=rotation,
            out=rotation_out,
            use_geometric_center=False,
            order=1,
        )
        projection = backend.sum(rotation_out, axis=-1)
        arr[..., 0] = projection

        projection_mask = backend.full(templateshape, dtype=real_dtype, fill_value=1)
        backend.fill(temp, 0)
        temp = backend.topleft_pad(projection_mask, temp.shape)

        template_mean = backend.mean(projection[subset])
        template_volume = backend.prod(projection[subset].shape)
        template_ssd = backend.sum(
            backend.square(backend.subtract(projection[subset], template_mean))
        )

        rfftn(temp, ft_temp)
        backend.multiply(ft_target, ft_temp, out=ft_denom)
        irfftn(ft_denom, temp)

        numerator = backend.multiply(temp, template_mean)

        backend.square(temp, out=temp)
        backend.divide(temp, template_volume, out=temp)
        backend.multiply(ft_target2, ft_temp, out=ft_denom)
        irfftn(ft_denom, temp2)

        backend.subtract(temp2, temp, out=temp)
        backend.multiply(temp, template_ssd, out=temp)
        backend.maximum(temp, 0.0, out=temp)
        backend.sqrt(temp, out=temp)

        denominator_mask = temp > backend.eps(temp.dtype)
        inv_denominator = backend.preallocate_array(fast_shape, real_dtype)
        inv_denominator[denominator_mask] = 1 / temp[denominator_mask]

        rfftn(arr, ft_temp)
        backend.multiply(ft_target, ft_temp, out=ft_temp)
        irfftn(ft_temp, arr)

        backend.subtract(arr, numerator, out=arr)
        backend.multiply(arr, inv_denominator, out=arr)

        convolution_mode = kwargs.get("convolution_mode", "full")
        score = apply_convolution_mode(
            arr, convolution_mode=convolution_mode, s1=targetshape, s2=templateshape
        )
        print(time() - start)
        if callback_class is not None:
            callback(
                score,
                rotation_matrix=rotation,
                rotation_index=index,
                **callback_class_args,
            )

    return callback


def corr3_setup(
    rfftn: Callable,
    irfftn: Callable,
    template: NDArray,
    template_mask: NDArray,
    target: NDArray,
    fast_shape: Tuple[int],
    fast_ft_shape: Tuple[int],
    real_dtype: type,
    complex_dtype: type,
    shared_memory_handler: Callable,
    callback_class: Callable,
    callback_class_args: Dict,
    **kwargs,
) -> Dict:
    target_pad = backend.topleft_pad(target, fast_shape)

    # The exact composition of the denominator is debatable
    # scikit-image match_template multiplies the running sum of the target
    # with a scaling factor derived from the template. This is probably appropriate
    # in pattern matching situations where the template exists in the target
    template_mask = backend.preallocate_array(
        (*template_mask.shape[:-1], 1), real_dtype
    )
    template_mask[:] = 1
    window_template = backend.topleft_pad(template_mask, fast_shape)
    ft_window_template = backend.preallocate_array(fast_ft_shape, complex_dtype)
    rfftn(window_template, ft_window_template)
    window_template = None

    # Target and squared target window sums
    ft_target = backend.preallocate_array(fast_ft_shape, complex_dtype)
    ft_target2 = backend.preallocate_array(fast_ft_shape, complex_dtype)
    denominator = backend.preallocate_array(fast_shape, real_dtype)
    target_window_sum = backend.preallocate_array(fast_shape, real_dtype)
    rfftn(target_pad, ft_target)

    rfftn(backend.square(target_pad), ft_target2)
    backend.multiply(ft_target2, ft_window_template, out=ft_target2)
    irfftn(ft_target2, denominator)

    backend.multiply(ft_target, ft_window_template, out=ft_window_template)
    irfftn(ft_window_template, target_window_sum)

    target_pad, ft_target2, ft_window_template = None, None, None

    projection = template.sum(axis=-1)
    # Normalizing constants
    template_mean = backend.mean(projection)
    template_volume = np.prod(projection.shape)
    template_ssd = backend.sum(
        backend.square(backend.subtract(projection, template_mean))
    )

    # Final numerator is score - numerator2
    numerator2 = backend.multiply(target_window_sum, template_mean)

    # Compute denominator
    backend.multiply(target_window_sum, target_window_sum, out=target_window_sum)
    backend.divide(target_window_sum, template_volume, out=target_window_sum)

    backend.subtract(denominator, target_window_sum, out=denominator)
    backend.multiply(denominator, template_ssd, out=denominator)
    backend.maximum(denominator, 0, out=denominator)
    backend.sqrt(denominator, out=denominator)
    target_window_sum = None

    # Invert denominator to compute final score as product
    denominator_mask = denominator > backend.eps(denominator.dtype)
    inv_denominator = backend.preallocate_array(fast_shape, real_dtype)
    inv_denominator[denominator_mask] = 1 / denominator[denominator_mask]

    # Convert arrays used in subsequent fitting to SharedMemory objects
    template_buffer = backend.arr_to_sharedarr(
        arr=template, shared_memory_handler=shared_memory_handler
    )
    target_ft_buffer = backend.arr_to_sharedarr(
        arr=ft_target, shared_memory_handler=shared_memory_handler
    )
    inv_denominator_buffer = backend.arr_to_sharedarr(
        arr=inv_denominator, shared_memory_handler=shared_memory_handler
    )
    numerator2_buffer = backend.arr_to_sharedarr(
        arr=numerator2, shared_memory_handler=shared_memory_handler
    )

    template_tuple = (template_buffer, deepcopy(template.shape), real_dtype)
    target_ft_tuple = (target_ft_buffer, fast_ft_shape, complex_dtype)

    inv_denominator_tuple = (inv_denominator_buffer, fast_shape, real_dtype)
    numerator2_tuple = (numerator2_buffer, fast_shape, real_dtype)

    ft_target, inv_denominator, numerator2 = None, None, None

    ret = {
        "template": template_tuple,
        "ft_target": target_ft_tuple,
        "inv_denominator": inv_denominator_tuple,
        "numerator2": numerator2_tuple,
        "targetshape": deepcopy(target.shape),
        "templateshape": deepcopy(template.shape),
        "fast_shape": fast_shape,
        "fast_ft_shape": fast_ft_shape,
        "real_dtype": real_dtype,
        "complex_dtype": complex_dtype,
        "callback_class": callback_class,
        "callback_class_args": callback_class_args,
        "template_mean": kwargs.get("template_mean", template_mean),
    }

    return ret


def corr3_scoring(
    template: Tuple[type, Tuple[int], type],
    ft_target: Tuple[type, Tuple[int], type],
    inv_denominator: Tuple[type, Tuple[int], type],
    numerator2: Tuple[type, Tuple[int], type],
    template_filter: Tuple[type, Tuple[int], type],
    targetshape: Tuple[int],
    templateshape: Tuple[int],
    fast_shape: Tuple[int],
    fast_ft_shape: Tuple[int],
    rotations: NDArray,
    real_dtype: type,
    complex_dtype: type,
    callback_class: CallbackClass,
    callback_class_args: Dict,
    interpolation_order: int,
    convolution_mode: str = "full",
    **kwargs,
) -> CallbackClass:
    template_buffer, template_shape, template_dtype = template
    ft_target_buffer, ft_target_shape, ft_target_dtype = ft_target
    inv_denominator_buffer, inv_denominator_pointer_shape, _ = inv_denominator
    numerator2_buffer, numerator2_shape, _ = numerator2
    filter_buffer, filter_shape, filter_dtype = template_filter

    if callback_class is not None and isinstance(callback_class, type):
        callback = callback_class(**callback_class_args)
    elif not isinstance(callback_class, type):
        callback = callback_class

    # Retrieve objects from shared memory
    template = backend.sharedarr_to_arr(template_shape, template_dtype, template_buffer)
    ft_target = backend.sharedarr_to_arr(
        ft_target_shape, ft_target_dtype, ft_target_buffer
    )
    inv_denominator = backend.sharedarr_to_arr(
        inv_denominator_pointer_shape, template_dtype, inv_denominator_buffer
    )
    numerator2 = backend.sharedarr_to_arr(
        numerator2_shape, template_dtype, numerator2_buffer
    )
    template_filter = backend.sharedarr_to_arr(
        filter_shape, filter_dtype, filter_buffer
    )

    arr = backend.preallocate_array(fast_shape, real_dtype)
    ft_temp = backend.preallocate_array(fast_ft_shape, complex_dtype)

    rfftn, irfftn = backend.build_fft(
        fast_shape=fast_shape,
        fast_ft_shape=fast_ft_shape,
        real_dtype=real_dtype,
        complex_dtype=complex_dtype,
        fftargs=kwargs.get("fftargs", {}),
        temp_real=arr,
        temp_fft=ft_temp,
    )

    norm_numerator = (backend.sum(numerator2) != 0) & (backend.size(numerator2) != 1)
    norm_denominator = (backend.sum(inv_denominator) != 1) & (
        backend.size(inv_denominator) != 1
    )
    filter_template = backend.size(template_filter) != 0

    norm_func_numerator = conditional_execute(backend.subtract, norm_numerator)
    norm_func_denominator = conditional_execute(backend.multiply, norm_denominator)
    template_filter_func = conditional_execute(backend.multiply, filter_template)

    rotation_out = backend.preallocate_array(
        (*fast_shape[:-1], template.shape[-1]), real_dtype
    )
    templateshape = list(templateshape)
    templateshape[-1] = 1
    from time import time

    for index in range(rotations.shape[0]):
        start = time()
        rotation = rotations[index]
        backend.fill(arr, 0)
        backend.rotate_array(
            arr=template,
            rotation_matrix=rotation,
            out=rotation_out,
            use_geometric_center=False,
            order=interpolation_order,
        )
        projection = backend.sum(rotation_out, axis=-1)
        arr[..., 0] = projection

        rfftn(arr, ft_temp)
        template_filter_func(ft_temp, template_filter, out=ft_temp)

        backend.multiply(ft_target, ft_temp, out=ft_temp)
        irfftn(ft_temp, arr)

        norm_func_numerator(arr, numerator2, out=arr)
        norm_func_denominator(arr, inv_denominator, out=arr)

        score = apply_convolution_mode(
            arr, convolution_mode=convolution_mode, s1=targetshape, s2=templateshape
        )
        print(time() - start)
        if callback_class is not None:
            callback(
                score,
                rotation_matrix=rotation,
                rotation_index=index,
                **callback_class_args,
            )

    return callback

@device_memory_handler
def scan(
    matching_data: MatchingData,
    matching_setup: Callable,
    matching_score: Callable,
    n_jobs: int = 4,
    callback_class: CallbackClass = None,
    callback_class_args: Dict = {},
    fftargs: Dict = {},
    pad_fourier: bool = True,
    interpolation_order: int = 3,
    jobs_per_callback_class: int = 8,
    **kwargs,
) -> Tuple:
    """
    Perform template matching between target and template and sample
    different rotations of template.

    Parameters
    ----------
    matching_data : MatchingData
        Template matching data.
    matching_setup : Callable
        Function pointer to setup function.
    matching_score : Callable
        Function pointer to scoring function.
    n_jobs : int, optional
        Number of parallel jobs. Default is 4.
    callback_class : type, optional
        Analyzer class pointer to operate on computed scores.
    callback_class_args : dict, optional
        Arguments passed to the callback_class. Default is an empty dictionary.
    fftargs : dict, optional
        Arguments for the FFT operations. Default is an empty dictionary.
    pad_fourier: bool, optional
        Whether to pad target and template to the full convolution shape.
    interpolation_order : int, optional
        Order of spline interpolation for rotations.
    jobs_per_callback_class : int, optional
        How many jobs should be processed by a single callback_class instance,
        if ones is provided.
    **kwargs : various
        Additional arguments.

    Returns
    -------
    Tuple
        The merged results from callback_class if provided otherwise None.
    """
    matching_data.to_backend()
    fourier_pad = matching_data._templateshape
    fourier_pad = list(matching_data._templateshape)
    fourier_pad[-1] = 1
    print("make sure to remove this")
    fourier_shift = backend.zeros(len(fourier_pad))
    if not pad_fourier:
        fourier_pad = backend.full(shape=fourier_shift.shape, fill_value=1, dtype=int)
        fourier_shift = 1 - backend.astype(
            backend.divide(matching_data._templateshape, 2), int
        )
        callback_class_args["fourier_shift"] = fourier_shift

    _, fast_shape, fast_ft_shape = backend.compute_convolution_shapes(
        matching_data._target.shape, fourier_pad
    )
    rfftn, irfftn = backend.build_fft(
        fast_shape=fast_shape,
        fast_ft_shape=fast_ft_shape,
        real_dtype=matching_data._default_dtype,
        complex_dtype=matching_data._complex_dtype,
        fftargs=fftargs,
    )
    setup = matching_setup(
        rfftn=rfftn,
        irfftn=irfftn,
        template=matching_data.template,
        template_mask=matching_data.template_mask,
        target=matching_data.target,
        target_mask=matching_data.target_mask,
        fast_shape=fast_shape,
        fast_ft_shape=fast_ft_shape,
        real_dtype=matching_data._default_dtype,
        complex_dtype=matching_data._complex_dtype,
        callback_class=callback_class,
        callback_class_args=callback_class_args,
        **kwargs,
    )
    rfftn, irfftn = None, None

    template_filter, preprocessor = None, Preprocessor()
    for method, parameters in matching_data.template_filter.items():
        parameters["shape"] = fast_shape
        parameters["omit_negative_frequencies"] = True
        out = preprocessor.apply_method(method=method, parameters=parameters)
        if template_filter is None:
            template_filter = out
        np.multiply(template_filter, out, out=template_filter)

    if template_filter is None:
        template_filter = backend.full(
            shape=(1,), fill_value=1, dtype=backend._default_dtype
        )
    else:
        template_filter = backend.to_backend_array(template_filter)

    template_filter = backend.astype(template_filter, backend._default_dtype)
    template_filter_buffer = backend.arr_to_sharedarr(
        arr=template_filter,
        shared_memory_handler=kwargs.get("shared_memory_handler", None),
    )
    setup["template_filter"] = (
        template_filter_buffer,
        template_filter.shape,
        template_filter.dtype,
    )

    callback_class_args["translation_offset"] = backend.astype(
        matching_data._translation_offset, int
    )
    callback_class_args["thread_safe"] = n_jobs > 1
    callback_class_args["gpu_index"] = kwargs.get("gpu_index", -1)

    n_callback_classes = max(n_jobs // jobs_per_callback_class, 1)
    callback_class = setup.pop("callback_class", callback_class)
    callback_class_args = setup.pop("callback_class_args", callback_class_args)
    callback_classes = [callback_class for _ in range(n_callback_classes)]
    if callback_class == MaxScoreOverRotations:
        score_space_shape = backend.subtract(
            matching_data.target.shape,
            matching_data._target_pad,
        )
        callback_classes = [
            class_name(
                score_space_shape=score_space_shape,
                score_space_dtype=matching_data._default_dtype,
                shared_memory_handler=kwargs.get("shared_memory_handler", None),
                rotation_space_dtype=backend._default_dtype_int,
                **callback_class_args,
            )
            for class_name in callback_classes
        ]

    matching_data._target, matching_data._template = None, None
    matching_data._target_mask, matching_data._template_mask = None, None

    setup["fftargs"] = fftargs.copy()
    convolution_mode = "same"
    if backend.sum(matching_data._target_pad) > 0:
        convolution_mode = "valid"
    setup["convolution_mode"] = convolution_mode
    setup["interpolation_order"] = interpolation_order
    rotation_list = matching_data._split_rotations_on_jobs(n_jobs)

    backend.free_cache()

    def _run_scoring(backend_name, backend_args, rotations, **kwargs):
        from tme.backends import backend

        backend.change_backend(backend_name, **backend_args)
        return matching_score(rotations=rotations, **kwargs)

    callbacks = Parallel(n_jobs=n_jobs)(
        delayed(_run_scoring)(
            backend_name=backend._backend_name,
            backend_args=backend._backend_args,
            rotations=rotation,
            callback_class=callback_classes[index % n_callback_classes],
            callback_class_args=callback_class_args,
            **setup,
        )
        for index, rotation in enumerate(rotation_list)
    )

    callbacks = [
        tuple(callback)
        for callback in callbacks[0:n_callback_classes]
        if callback is not None
    ]
    backend.free_cache()

    merged_callback = None
    if callback_class is not None:
        merged_callback = callback_class.merge(
            callbacks,
            **callback_class_args,
            score_indices=matching_data.indices,
            inner_merge=True,
        )

    return merged_callback


register_matching_exhaustive(
    matching = "CC2",
    matching_setup = corr2_setup,
    matching_scoring = corr2_scoring,
    memory_class = CCMemoryUsage)

register_matching_exhaustive(
    matching = "CC3",
    matching_setup = corr3_setup,
    matching_scoring = corr3_scoring,
    memory_class = CCMemoryUsage
)
