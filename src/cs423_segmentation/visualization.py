"""Mask and overlay generation helpers."""

from __future__ import annotations

from pathlib import Path
from typing import Union

import numpy as np
from PIL import Image


def save_mask_image(mask: np.ndarray, path: Union[str, Path]) -> None:
    destination = Path(path)
    destination.parent.mkdir(parents=True, exist_ok=True)
    mask_image = Image.fromarray(mask.astype(np.uint8) * 255)
    mask_image.save(destination)


def save_overlay_image(image: np.ndarray, mask: np.ndarray, path: Union[str, Path]) -> None:
    destination = Path(path)
    destination.parent.mkdir(parents=True, exist_ok=True)
    overlay = image.copy().astype(np.uint8)
    highlight = np.array([255, 255, 0], dtype=np.uint8)
    overlay[mask] = ((0.5 * overlay[mask]) + (0.5 * highlight)).astype(np.uint8)
    Image.fromarray(overlay).save(destination)
