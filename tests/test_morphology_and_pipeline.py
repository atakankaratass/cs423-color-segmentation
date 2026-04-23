import numpy as np

from cs423_segmentation.morphology import opening
from cs423_segmentation.pipeline import run_pipeline


def test_opening_removes_isolated_noise_pixel() -> None:
    mask = np.zeros((5, 5), dtype=bool)
    mask[2, 2] = True
    cleaned = opening(mask, kernel_size=3, iterations=1)
    assert not cleaned.any()


def test_rgb_pipeline_counts_two_objects_in_sample_like_image() -> None:
    image = np.array(
        [
            [[255, 255, 255], [255, 0, 0], [255, 0, 0], [255, 255, 255], [255, 0, 0], [255, 0, 0]],
            [[255, 255, 255], [255, 0, 0], [255, 0, 0], [255, 255, 255], [255, 0, 0], [255, 0, 0]],
            [
                [255, 255, 255],
                [255, 255, 255],
                [255, 255, 255],
                [255, 255, 255],
                [255, 255, 255],
                [255, 255, 255],
            ],
        ],
        dtype=np.uint8,
    )
    result = run_pipeline(
        image,
        {
            "color_space": "rgb",
            "lower": [200, 0, 0],
            "upper": [255, 80, 80],
            "morphology": {"kernel_size": 1, "opening_iterations": 1, "closing_iterations": 1},
            "min_component_size": 2,
        },
    )
    assert result.count == 2
    assert sorted(result.component_sizes) == [4, 4]


def test_hsv_pipeline_keeps_dim_red_object_when_value_threshold_allows_it() -> None:
    image = np.array(
        [[[120, 0, 0], [255, 255, 255]], [[120, 0, 0], [255, 255, 255]]], dtype=np.uint8
    )
    result = run_pipeline(
        image,
        {
            "color_space": "hsv",
            "ranges": [
                {"lower": [0, 120, 50], "upper": [10, 255, 255]},
                {"lower": [170, 120, 50], "upper": [179, 255, 255]},
            ],
            "morphology": {"kernel_size": 1, "opening_iterations": 1, "closing_iterations": 1},
            "min_component_size": 1,
        },
    )
    assert result.count == 1


def test_hsv_edge_refinement_filters_out_flat_false_positive_region() -> None:
    image = np.array(
        [
            [
                [255, 255, 255],
                [255, 255, 255],
                [255, 255, 255],
                [255, 255, 255],
                [220, 40, 40],
                [220, 40, 40],
            ],
            [
                [255, 255, 255],
                [255, 0, 0],
                [100, 0, 0],
                [255, 255, 255],
                [220, 40, 40],
                [220, 40, 40],
            ],
            [
                [255, 255, 255],
                [255, 0, 0],
                [100, 0, 0],
                [255, 255, 255],
                [220, 40, 40],
                [220, 40, 40],
            ],
            [
                [255, 255, 255],
                [255, 255, 255],
                [255, 255, 255],
                [255, 255, 255],
                [220, 40, 40],
                [220, 40, 40],
            ],
        ],
        dtype=np.uint8,
    )
    result = run_pipeline(
        image,
        {
            "color_space": "hsv",
            "ranges": [
                {"lower": [0, 100, 50], "upper": [10, 255, 255]},
                {"lower": [170, 100, 50], "upper": [179, 255, 255]},
            ],
            "morphology": {"kernel_size": 1, "opening_iterations": 1, "closing_iterations": 1},
            "min_component_size": 1,
            "refinement": {
                "type": "edge_supported",
                "gradient_threshold": 40,
                "min_edge_fraction": 0.3,
            },
        },
    )
    assert result.count == 1
    assert result.component_sizes == [4]
