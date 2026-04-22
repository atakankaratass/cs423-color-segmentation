import numpy as np

from cs423_segmentation.color import rgb_to_hsv, threshold_hsv, threshold_rgb


def test_rgb_to_hsv_maps_red_to_low_hue() -> None:
    image = np.array([[[255, 0, 0]]], dtype=np.uint8)
    hsv = rgb_to_hsv(image)
    assert int(hsv[0, 0, 0]) == 0
    assert int(hsv[0, 0, 1]) == 255
    assert int(hsv[0, 0, 2]) == 255


def test_threshold_rgb_selects_red_pixels() -> None:
    image = np.array([[[255, 0, 0], [20, 30, 40]]], dtype=np.uint8)
    mask = threshold_rgb(image, lower=(200, 0, 0), upper=(255, 80, 80))
    assert mask.tolist() == [[True, False]]


def test_threshold_hsv_supports_multiple_ranges_for_red() -> None:
    image = np.array([[[255, 0, 0], [10, 10, 10]]], dtype=np.uint8)
    mask = threshold_hsv(
        image,
        ranges=[
            {"lower": (0, 120, 80), "upper": (10, 255, 255)},
            {"lower": (170, 120, 80), "upper": (179, 255, 255)},
        ],
    )
    assert mask.tolist() == [[True, False]]
