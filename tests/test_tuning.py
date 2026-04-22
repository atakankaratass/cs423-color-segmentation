import csv
from pathlib import Path

from cs423_segmentation.tuning import build_candidate_profiles, tune_profile


def test_build_candidate_profiles_for_rgb_creates_multiple_candidates() -> None:
    candidates = build_candidate_profiles(
        "rgb_red",
        {
            "color_space": "rgb",
            "lower": [200, 0, 0],
            "upper": [255, 80, 80],
            "morphology": {"kernel_size": 1, "opening_iterations": 1, "closing_iterations": 1},
            "min_component_size": 2,
        },
    )
    assert len(candidates) == 4
    assert candidates[0][0] == "rgb_red-base"


def test_tune_profile_writes_ranked_outputs(tmp_path: Path) -> None:
    result = tune_profile("data/sample/metadata/dataset.json", "hsv_red", tmp_path)
    csv_path = tmp_path / "tuning-results.csv"
    markdown_path = tmp_path / "tuning-results.md"
    assert result["best_candidate"].startswith("hsv_red-")
    assert result["rankings"][0]["exact_match_accuracy"] == 1.0
    assert csv_path.exists()
    assert markdown_path.exists()

    with csv_path.open("r", encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))
    assert rows[0]["candidate"].startswith("hsv_red-")
