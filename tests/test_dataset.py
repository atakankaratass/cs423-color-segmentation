import json
from pathlib import Path

import pytest

from cs423_segmentation.dataset import load_dataset_metadata, load_profile_set, validate_dataset


def test_load_dataset_metadata_reads_required_fields() -> None:
    metadata = load_dataset_metadata("data/sample/metadata/dataset.json")
    assert metadata["metadata_schema_version"] == "v1"
    assert metadata["images"][0]["lighting"] == "controlled"


def test_load_profile_set_reads_versioned_profile_config() -> None:
    profile_set = load_profile_set("data/sample/metadata/dataset.json")
    assert profile_set["profile_set_version"] == "v1"
    assert set(profile_set["profiles"]) == {"rgb_red", "hsv_red"}


def test_load_dataset_metadata_rejects_missing_required_keys(tmp_path: Path) -> None:
    broken_metadata = tmp_path / "dataset.json"
    broken_metadata.write_text(
        json.dumps({"dataset_name": "broken", "images": []}), encoding="utf-8"
    )
    with pytest.raises(ValueError):
        load_dataset_metadata(broken_metadata)


def test_validate_dataset_accepts_sample_metadata() -> None:
    result = validate_dataset("data/sample/metadata/dataset.json")
    assert result["is_valid"] is True
    assert result["checked_images"] == 2


def test_validate_dataset_reports_missing_image_file(tmp_path: Path) -> None:
    metadata_path = tmp_path / "dataset.json"
    metadata_path.write_text(
        json.dumps(
            {
                "dataset_name": "broken",
                "metadata_schema_version": "v1",
                "profile_set_path": "configs/profiles/v1/red-segmentation.json",
                "images": [
                    {
                        "image_id": "broken-001",
                        "image_path": "data/real/raw/missing.ppm",
                        "target_color": "red",
                        "expected_count": 1,
                        "lighting": "controlled",
                        "background": "plain",
                        "overlap": "none",
                    }
                ],
            }
        ),
        encoding="utf-8",
    )
    result = validate_dataset(metadata_path)
    assert result["is_valid"] is False
    assert any("Missing image file" in error for error in result["errors"])
