"""Dataset metadata and profile loading helpers."""

from __future__ import annotations

from pathlib import Path
from typing import Any, Union

from cs423_segmentation.io_utils import load_json

ALLOWED_LIGHTING = {"controlled", "dim", "bright"}
ALLOWED_BACKGROUND = {"plain", "cluttered"}
ALLOWED_OVERLAP = {"none", "mild", "heavy"}


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


def validate_dataset(metadata_path: Union[str, Path]) -> dict[str, Any]:
    metadata_file = Path(metadata_path).resolve()
    repository_root = metadata_file.parents[3]
    try:
        metadata = load_dataset_metadata(metadata_file)
    except ValueError as error:
        return {
            "dataset_name": metadata_file.stem,
            "checked_images": 0,
            "is_valid": False,
            "errors": [str(error)],
        }

    image_ids: set[str] = set()
    errors: list[str] = []
    checked_images = 0

    for item in metadata["images"]:
        checked_images += 1
        image_id = item["image_id"]
        if image_id in image_ids:
            errors.append(f"Duplicate image_id: {image_id}")
        image_ids.add(image_id)

        image_path = repository_root / item["image_path"]
        if not image_path.exists():
            errors.append(f"Missing image file: {item['image_path']}")

        if item["lighting"] not in ALLOWED_LIGHTING:
            errors.append(f"Invalid lighting label for {image_id}: {item['lighting']}")
        if item["background"] not in ALLOWED_BACKGROUND:
            errors.append(f"Invalid background label for {image_id}: {item['background']}")
        if item["overlap"] not in ALLOWED_OVERLAP:
            errors.append(f"Invalid overlap label for {image_id}: {item['overlap']}")
        if int(item["expected_count"]) < 0:
            errors.append(f"Negative expected_count for {image_id}")

    try:
        profile_set = load_profile_set(metadata_file)
    except (ValueError, FileNotFoundError) as error:
        errors.append(str(error))
    else:
        if not profile_set["profiles"]:
            errors.append("Profile set contains no profiles.")

    return {
        "dataset_name": metadata["dataset_name"],
        "checked_images": checked_images,
        "is_valid": not errors,
        "errors": errors,
    }


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
