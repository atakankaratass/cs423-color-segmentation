import json
from pathlib import Path

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
