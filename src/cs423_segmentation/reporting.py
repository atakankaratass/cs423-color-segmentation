"""Report generation helpers for experiment summaries and artifacts."""

from __future__ import annotations

from collections import defaultdict
from pathlib import Path
from typing import Any, Optional, Union

from cs423_segmentation.dataset import load_dataset_metadata, load_profile_set
from cs423_segmentation.evaluation import evaluate_dataset, run_experiments
from cs423_segmentation.io_utils import load_image, save_csv, save_text
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
    save_text(
        report_root / "profile-summary.md",
        build_markdown_table(
            experiment_summary["profiles"],
            ["profile", "exact_match_accuracy", "mean_absolute_error", "average_runtime_ms"],
            {
                "profile": "Profile",
                "exact_match_accuracy": "Exact Match Accuracy",
                "mean_absolute_error": "Mean Absolute Error",
                "average_runtime_ms": "Average Runtime (ms)",
            },
        ),
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
    save_text(
        report_root / "condition-summary.md",
        build_markdown_table(
            condition_rows,
            [
                "profile",
                "condition_type",
                "condition_value",
                "image_count",
                "exact_match_accuracy",
                "mean_absolute_error",
            ],
            {
                "profile": "Profile",
                "condition_type": "Condition Type",
                "condition_value": "Condition Value",
                "image_count": "Image Count",
                "exact_match_accuracy": "Exact Match Accuracy",
                "mean_absolute_error": "Mean Absolute Error",
            },
        ),
    )

    error_rows = build_error_rows(detail_summaries)
    worst_case_rows = build_worst_case_rows(detail_summaries)
    error_type_rows = build_error_type_rows(detail_summaries)

    save_csv(
        report_root / "error-analysis.csv",
        [
            "profile",
            "image_id",
            "image_path",
            "target_color",
            "expected_count",
            "predicted_count",
            "absolute_error",
            "false_positives",
            "false_negatives",
            "lighting",
            "background",
            "overlap",
        ],
        error_rows,
    )
    save_text(
        report_root / "error-analysis.md",
        build_markdown_table(
            error_rows,
            [
                "profile",
                "image_id",
                "target_color",
                "expected_count",
                "predicted_count",
                "absolute_error",
                "false_positives",
                "false_negatives",
            ],
            {
                "profile": "Profile",
                "image_id": "Image ID",
                "target_color": "Color",
                "expected_count": "Expected",
                "predicted_count": "Predicted",
                "absolute_error": "Abs Error",
                "false_positives": "FP",
                "false_negatives": "FN",
            },
        ),
    )

    save_csv(
        report_root / "worst-cases.csv",
        [
            "profile",
            "image_id",
            "absolute_error",
            "false_positives",
            "false_negatives",
            "lighting",
            "background",
            "overlap",
        ],
        worst_case_rows,
    )
    save_text(
        report_root / "worst-cases.md",
        build_markdown_table(
            worst_case_rows,
            [
                "profile",
                "image_id",
                "absolute_error",
                "false_positives",
                "false_negatives",
                "lighting",
                "background",
                "overlap",
            ],
            {
                "profile": "Profile",
                "image_id": "Image ID",
                "absolute_error": "Abs Error",
                "false_positives": "FP",
                "false_negatives": "FN",
                "lighting": "Lighting",
                "background": "Background",
                "overlap": "Overlap",
            },
        ),
    )

    save_csv(
        report_root / "error-type-summary.csv",
        ["profile", "error_type", "image_count", "rate"],
        error_type_rows,
    )
    save_text(
        report_root / "error-type-summary.md",
        build_markdown_table(
            error_type_rows,
            ["profile", "error_type", "image_count", "rate"],
            {
                "profile": "Profile",
                "error_type": "Error Type",
                "image_count": "Image Count",
                "rate": "Rate",
            },
        ),
    )

    _write_visualizations(metadata_file, profile_set["profiles"], selected_profiles, report_root)
    return {
        "experiment_summary": experiment_summary,
        "condition_rows": condition_rows,
        "error_rows": error_rows,
        "worst_case_rows": worst_case_rows,
        "error_type_rows": error_type_rows,
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


def build_markdown_table(
    rows: list[dict[str, Any]], fieldnames: list[str], labels: dict[str, str]
) -> str:
    header = "| " + " | ".join(labels[field] for field in fieldnames) + " |"
    divider = (
        "| "
        + " | ".join("---:" if field != fieldnames[0] else "---" for field in fieldnames)
        + " |"
    )
    body = []
    for row in rows:
        body.append(
            "| " + " | ".join(_format_markdown_value(row[field]) for field in fieldnames) + " |"
        )
    return "\n".join([header, divider, *body]) + "\n"


def build_error_rows(detail_summaries: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for summary in detail_summaries:
        for item in summary["per_image"]:
            if item["absolute_error"] == 0:
                continue
            rows.append({"profile": summary["profile"], **item})
    rows.sort(
        key=lambda row: (
            row["profile"],
            -row["absolute_error"],
            -row["false_negatives"],
            -row["false_positives"],
            row["image_id"],
        )
    )
    return rows


def build_worst_case_rows(
    detail_summaries: list[dict[str, Any]], limit_per_profile: int = 3
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    error_rows = build_error_rows(detail_summaries)
    grouped: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in error_rows:
        grouped[row["profile"]].append(row)

    for _profile, items in sorted(grouped.items()):
        rows.extend(items[:limit_per_profile])
    return rows


def build_error_type_rows(detail_summaries: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for summary in detail_summaries:
        total_images = len(summary["per_image"])
        exact = 0
        overcount = 0
        undercount = 0
        mixed = 0
        for item in summary["per_image"]:
            if item["absolute_error"] == 0:
                exact += 1
            elif item["false_positives"] > 0 and item["false_negatives"] > 0:
                mixed += 1
            elif item["false_positives"] > 0:
                overcount += 1
            else:
                undercount += 1

        for error_type, image_count in (
            ("exact", exact),
            ("overcount", overcount),
            ("undercount", undercount),
            ("mixed", mixed),
        ):
            rows.append(
                {
                    "profile": summary["profile"],
                    "error_type": error_type,
                    "image_count": image_count,
                    "rate": image_count / total_images if total_images else 0.0,
                }
            )
    return rows


def _format_markdown_value(value: Any) -> str:
    if isinstance(value, float):
        return f"{value:.4f}"
    return str(value)


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
