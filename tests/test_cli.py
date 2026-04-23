import json
from io import StringIO
from pathlib import Path
from unittest.mock import patch

from cs423_segmentation.cli import build_parser, main


def test_parser_requires_subcommand() -> None:
    parser = build_parser()
    try:
        parser.parse_args([])
    except SystemExit as error:
        assert error.code == 2
    else:
        raise AssertionError("Parser should require a subcommand.")


def test_cli_evaluates_sample_dataset(tmp_path: Path) -> None:
    output_path = tmp_path / "rgb-results.json"
    exit_code = main(
        [
            "evaluate",
            "--metadata",
            "data/sample/metadata/dataset.json",
            "--profile",
            "rgb_red",
            "--output",
            str(output_path),
        ]
    )
    payload = json.loads(output_path.read_text(encoding="utf-8"))
    assert exit_code == 0
    assert payload["image_count"] == 2
    assert payload["exact_match_accuracy"] == 0.5
    assert payload["mean_absolute_error"] == 0.5


def test_cli_runs_experiment_summary(tmp_path: Path) -> None:
    output_path = tmp_path / "summary.json"
    exit_code = main(
        [
            "run-experiments",
            "--metadata",
            "data/sample/metadata/dataset.json",
            "--output",
            str(output_path),
        ]
    )
    payload = json.loads(output_path.read_text(encoding="utf-8"))
    assert exit_code == 0
    assert payload["metadata_schema_version"] == "v1"
    assert payload["profile_set_version"] == "v1"
    assert [item["profile"] for item in payload["profiles"]] == ["hsv_red", "rgb_red"]


def test_cli_build_bundle_reports_validation_errors_cleanly(tmp_path: Path) -> None:
    metadata_path = tmp_path / "dataset.json"
    metadata_path.write_text(json.dumps({"dataset_name": "broken", "images": []}), encoding="utf-8")
    output_path = tmp_path / "bundle"
    stderr = StringIO()
    with patch("sys.stderr", stderr):
        exit_code = main(
            [
                "build-bundle",
                "--metadata",
                str(metadata_path),
                "--output-dir",
                str(output_path),
                "--skip-tuning",
            ]
        )

    assert exit_code == 1
    assert "Dataset validation failed" in stderr.getvalue()


def test_cli_build_bundle_reports_missing_metadata_cleanly(tmp_path: Path) -> None:
    output_path = tmp_path / "bundle"
    stderr = StringIO()
    with patch("sys.stderr", stderr):
        exit_code = main(
            [
                "build-bundle",
                "--metadata",
                str(tmp_path / "missing.json"),
                "--output-dir",
                str(output_path),
                "--skip-tuning",
            ]
        )

    assert exit_code == 1
    assert "missing.json" in stderr.getvalue()
