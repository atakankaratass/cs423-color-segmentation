"""Report generation helpers for experiment summaries and artifacts."""

from __future__ import annotations

from collections import defaultdict
from pathlib import Path
from typing import Any, Optional, Union

from cs423_segmentation.dataset import load_dataset_metadata, load_profile_set
from cs423_segmentation.evaluation import evaluate_dataset, run_experiments
from cs423_segmentation.io_utils import load_image, save_csv
from cs423_segmentation.pipeline import run_pipeline
from cs423_segmentation.visualization import save_mask_image, save_overlay_image


def generate_report(
    metadata_path: Union[str, Path],
    output_dir: Union[str, Path],
    profile_names: Optional[list[str]] = None,
) -> dict[str, Any]:
    metadata_file = Path(metadata_path).resolve()
    profile_set = load_profile_set(metadata_file)
    selected_profiles = profile_names or sorted(profile_set["profiles"])
    report_root = Path(output_dir)
    report_root.mkdir(parents=True, exist_ok=True)

    experiment_summary = run_experiments(
        metadata_file, report_root / "experiment-summary.json", selected_profiles
    )
    detail_summaries = [
        evaluate_dataset(metadata_file, profile_name, report_root / f"{profile_name}-detail.json")
        for profile_name in selected_profiles
    ]

    save_csv(
        report_root / "profile-summary.csv",
        ["profile", "exact_match_accuracy", "mean_absolute_error", "average_runtime_ms"],
        experiment_summary["profiles"],
    )

    condition_rows = build_condition_summary_rows(detail_summaries)
    save_csv(
        report_root / "condition-summary.csv",
        [
            "profile",
            "condition_type",
            "condition_value",
            "image_count",
            "exact_match_accuracy",
            "mean_absolute_error",
        ],
        condition_rows,
    )

    _write_visualizations(metadata_file, profile_set["profiles"], selected_profiles, report_root)
    return {
        "experiment_summary": experiment_summary,
        "condition_rows": condition_rows,
        "output_dir": str(report_root),
    }


def build_condition_summary_rows(detail_summaries: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for summary in detail_summaries:
        for condition_type in ("lighting", "background", "overlap"):
            grouped: dict[str, list[dict[str, Any]]] = defaultdict(list)
            for item in summary["per_image"]:
                grouped[item[condition_type]].append(item)

            for condition_value, items in sorted(grouped.items()):
                exact_matches = sum(int(item["absolute_error"] == 0) for item in items)
                mean_absolute_error = sum(item["absolute_error"] for item in items) / len(items)
                rows.append(
                    {
                        "profile": summary["profile"],
                        "condition_type": condition_type,
                        "condition_value": condition_value,
                        "image_count": len(items),
                        "exact_match_accuracy": exact_matches / len(items),
                        "mean_absolute_error": mean_absolute_error,
                    }
                )
    return rows


def _write_visualizations(
    metadata_path: Path,
    profiles: dict[str, dict[str, Any]],
    selected_profiles: list[str],
    report_root: Path,
) -> None:
    metadata = load_dataset_metadata(metadata_path)
    dataset_root = metadata_path.parents[3]

    for item in metadata["images"]:
        image = load_image(dataset_root / item["image_path"])
        for profile_name in selected_profiles:
            result = run_pipeline(image, profiles[profile_name])
            base_name = f"{item['image_id']}-{profile_name}"
            save_mask_image(result.mask, report_root / "masks" / f"{base_name}.png")
            save_overlay_image(image, result.mask, report_root / "overlays" / f"{base_name}.png")
