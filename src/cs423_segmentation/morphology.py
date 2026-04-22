"""Binary morphology helpers for segmentation cleanup."""

from __future__ import annotations

import numpy as np
from numpy.lib.stride_tricks import sliding_window_view


def dilate(mask: np.ndarray, kernel_size: int = 3, iterations: int = 1) -> np.ndarray:
    return _apply_morphology(mask, kernel_size, iterations, require_all=False)


def erode(mask: np.ndarray, kernel_size: int = 3, iterations: int = 1) -> np.ndarray:
    return _apply_morphology(mask, kernel_size, iterations, require_all=True)


def opening(mask: np.ndarray, kernel_size: int = 3, iterations: int = 1) -> np.ndarray:
    return dilate(
        erode(mask, kernel_size=kernel_size, iterations=iterations), kernel_size, iterations
    )


def closing(mask: np.ndarray, kernel_size: int = 3, iterations: int = 1) -> np.ndarray:
    return erode(
        dilate(mask, kernel_size=kernel_size, iterations=iterations), kernel_size, iterations
    )


def _apply_morphology(
    mask: np.ndarray,
    kernel_size: int,
    iterations: int,
    require_all: bool,
) -> np.ndarray:
    if mask.ndim != 2:
        raise ValueError("Morphology expects a 2D mask.")
    if kernel_size % 2 == 0 or kernel_size < 1:
        raise ValueError("kernel_size must be a positive odd integer.")

    result = mask.astype(bool)
    for _ in range(iterations):
        padding = kernel_size // 2
        padded = np.pad(result, padding, mode="constant", constant_values=False)
        windows = sliding_window_view(padded, (kernel_size, kernel_size))
        result = np.all(windows, axis=(-1, -2)) if require_all else np.any(windows, axis=(-1, -2))
    return result
