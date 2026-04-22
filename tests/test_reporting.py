import csv
from pathlib import Path

from cs423_segmentation.reporting import build_condition_summary_rows, generate_report


def test_build_condition_summary_rows_groups_by_condition() -> None:
    rows = build_condition_summary_rows(
        [
            {
                "profile": "rgb_red",
                "per_image": [
                    {
                        "lighting": "controlled",
                        "background": "plain",
                        "overlap": "none",
                        "absolute_error": 0,
                    },
                    {
                        "lighting": "dim",
                        "background": "plain",
                        "overlap": "none",
                        "absolute_error": 1,
                    },
                ],
            }
        ]
    )
    assert any(
        row["condition_type"] == "lighting" and row["condition_value"] == "controlled"
        for row in rows
    )
    assert any(
        row["condition_type"] == "lighting" and row["condition_value"] == "dim" for row in rows
    )


def test_generate_report_writes_csv_and_visualization_artifacts(tmp_path: Path) -> None:
    report = generate_report("data/sample/metadata/dataset.json", tmp_path)
    profile_summary = tmp_path / "profile-summary.csv"
    condition_summary = tmp_path / "condition-summary.csv"
    mask_image = tmp_path / "masks" / "sample-001-hsv_red.png"
    overlay_image = tmp_path / "overlays" / "sample-001-hsv_red.png"

    assert report["experiment_summary"]["profile_set_version"] == "v1"
    assert profile_summary.exists()
    assert condition_summary.exists()
    assert mask_image.exists()
    assert overlay_image.exists()

    with profile_summary.open("r", encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))
    assert [row["profile"] for row in rows] == ["hsv_red", "rgb_red"]
