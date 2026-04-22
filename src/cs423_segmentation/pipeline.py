"""Core segmentation pipelines for RGB and HSV thresholding."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import numpy as np

from cs423_segmentation.color import threshold_hsv, threshold_rgb
from cs423_segmentation.counting import count_connected_components
from cs423_segmentation.morphology import closing, opening


@dataclass
class PipelineResult:
    count: int
    component_sizes: list[int]
    mask: np.ndarray


def run_pipeline(image: np.ndarray, config: dict[str, Any]) -> PipelineResult:
    color_space = config["color_space"].lower()
    morphology_config = config.get("morphology", {})
    min_component_size = int(config.get("min_component_size", 1))

    if color_space == "rgb":
        mask = threshold_rgb(image, config["lower"], config["upper"])
    elif color_space == "hsv":
        mask = threshold_hsv(image, config["ranges"])
    else:
        raise ValueError(f"Unsupported color space: {color_space}")

    opened = opening(
        mask,
        kernel_size=int(morphology_config.get("kernel_size", 3)),
        iterations=int(morphology_config.get("opening_iterations", 1)),
    )
    cleaned = closing(
        opened,
        kernel_size=int(morphology_config.get("kernel_size", 3)),
        iterations=int(morphology_config.get("closing_iterations", 1)),
    )

    count, component_sizes = count_connected_components(
        cleaned, min_component_size=min_component_size
    )
    return PipelineResult(count=count, component_sizes=component_sizes, mask=cleaned)
