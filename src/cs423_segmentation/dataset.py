"""Dataset metadata and profile loading helpers."""

from __future__ import annotations

from pathlib import Path
from typing import Any, Union

from cs423_segmentation.io_utils import load_json


def load_dataset_metadata(metadata_path: Union[str, Path]) -> dict[str, Any]:
    metadata = load_json(metadata_path)
    required_top_level = {"dataset_name", "metadata_schema_version", "profile_set_path", "images"}
    missing = required_top_level.difference(metadata)
    if missing:
        raise ValueError(f"Dataset metadata is missing required keys: {sorted(missing)}")

    for item in metadata["images"]:
        required_image_keys = {
            "image_id",
            "image_path",
            "target_color",
            "expected_count",
            "lighting",
            "background",
            "overlap",
        }
        missing_image_keys = required_image_keys.difference(item)
        if missing_image_keys:
            image_id = item.get("image_id", "<unknown>")
            missing_keys_list = sorted(missing_image_keys)
            raise ValueError(f"Dataset item {image_id} is missing keys: {missing_keys_list}")
    return metadata


def load_profile_set(metadata_path: Union[str, Path]) -> dict[str, Any]:
    metadata_file = Path(metadata_path).resolve()
    repository_root = metadata_file.parents[3]
    metadata = load_dataset_metadata(metadata_file)
    profile_set = load_json(repository_root / metadata["profile_set_path"])
    required_keys = {"profile_set_name", "profile_set_version", "profiles"}
    missing = required_keys.difference(profile_set)
    if missing:
        raise ValueError(f"Profile set is missing required keys: {sorted(missing)}")
    return profile_set
