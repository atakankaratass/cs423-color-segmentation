"""Color-space conversions and thresholding helpers."""

from __future__ import annotations

from typing import Iterable

import numpy as np


def ensure_uint8_image(image: np.ndarray) -> np.ndarray:
    if image.ndim != 3 or image.shape[2] != 3:
        raise ValueError("Expected an HxWx3 image array.")
    if image.dtype != np.uint8:
        raise ValueError("Expected image dtype uint8.")
    return image


def rgb_to_hsv(image: np.ndarray) -> np.ndarray:
    """Convert an RGB uint8 image to OpenCV-style HSV ranges."""

    rgb = ensure_uint8_image(image).astype(np.float32) / 255.0
    red = rgb[..., 0]
    green = rgb[..., 1]
    blue = rgb[..., 2]

    max_value = np.max(rgb, axis=-1)
    min_value = np.min(rgb, axis=-1)
    delta = max_value - min_value

    hue = np.zeros_like(max_value)
    non_zero_delta = delta != 0

    red_is_max = non_zero_delta & (max_value == red)
    green_is_max = non_zero_delta & (max_value == green)
    blue_is_max = non_zero_delta & (max_value == blue)

    hue[red_is_max] = ((green[red_is_max] - blue[red_is_max]) / delta[red_is_max]) % 6.0
    hue[green_is_max] = ((blue[green_is_max] - red[green_is_max]) / delta[green_is_max]) + 2.0
    hue[blue_is_max] = ((red[blue_is_max] - green[blue_is_max]) / delta[blue_is_max]) + 4.0
    hue = (hue * 30.0).round().astype(np.uint8)

    saturation = np.zeros_like(max_value)
    non_zero_max = max_value != 0
    saturation[non_zero_max] = delta[non_zero_max] / max_value[non_zero_max]
    saturation = (saturation * 255.0).round().astype(np.uint8)

    value = (max_value * 255.0).round().astype(np.uint8)

    return np.stack([hue, saturation, value], axis=-1)


def threshold_rgb(image: np.ndarray, lower: Iterable[int], upper: Iterable[int]) -> np.ndarray:
    rgb = ensure_uint8_image(image)
    lower_array = np.asarray(tuple(lower), dtype=np.uint8)
    upper_array = np.asarray(tuple(upper), dtype=np.uint8)
    if lower_array.shape != (3,) or upper_array.shape != (3,):
        raise ValueError("RGB threshold bounds must contain exactly three integers.")
    return np.all((rgb >= lower_array) & (rgb <= upper_array), axis=-1)


def threshold_hsv(image: np.ndarray, ranges: list[dict[str, Iterable[int]]]) -> np.ndarray:
    hsv = rgb_to_hsv(image)
    mask = np.zeros(hsv.shape[:2], dtype=bool)
    for threshold_range in ranges:
        lower_array = np.asarray(tuple(threshold_range["lower"]), dtype=np.uint8)
        upper_array = np.asarray(tuple(threshold_range["upper"]), dtype=np.uint8)
        if lower_array.shape != (3,) or upper_array.shape != (3,):
            raise ValueError("HSV threshold bounds must contain exactly three integers.")
        current = np.all((hsv >= lower_array) & (hsv <= upper_array), axis=-1)
        mask |= current
    return mask
