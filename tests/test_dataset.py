import json
from pathlib import Path

import pytest

from cs423_segmentation.dataset import load_dataset_metadata, load_profile_set


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
