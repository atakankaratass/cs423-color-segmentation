"""Profile tuning helpers for trying small threshold variations automatically."""

from __future__ import annotations

from copy import deepcopy
from pathlib import Path
from typing import Any, Union

from cs423_segmentation.dataset import load_profile_set
from cs423_segmentation.evaluation import evaluate_dataset_summary
from cs423_segmentation.io_utils import save_csv, save_json, save_text


def tune_profile(
    metadata_path: Union[str, Path],
    source_profile_name: str,
    output_dir: Union[str, Path],
) -> dict[str, Any]:
    metadata_file = Path(metadata_path).resolve()
    profile_set = load_profile_set(metadata_file)
    source_profile = profile_set["profiles"][source_profile_name]
    candidates = build_candidate_profiles(source_profile_name, source_profile)
    destination = Path(output_dir)
    destination.mkdir(parents=True, exist_ok=True)

    rankings = []
    for candidate_name, candidate_profile in candidates:
        summary = evaluate_dataset_summary(metadata_file, candidate_name, candidate_profile)
        rankings.append(
            {
                "candidate": candidate_name,
                "exact_match_accuracy": summary["exact_match_accuracy"],
                "mean_absolute_error": summary["mean_absolute_error"],
                "average_runtime_ms": summary["average_runtime_ms"],
                "profile": candidate_profile,
            }
        )

    rankings.sort(
        key=lambda item: (
            -item["exact_match_accuracy"],
            item["mean_absolute_error"],
            item["average_runtime_ms"],
        )
    )

    save_json(destination / "tuning-results.json", rankings)
    csv_rows = [
        {
            "candidate": item["candidate"],
            "exact_match_accuracy": item["exact_match_accuracy"],
            "mean_absolute_error": item["mean_absolute_error"],
            "average_runtime_ms": item["average_runtime_ms"],
        }
        for item in rankings
    ]
    save_csv(
        destination / "tuning-results.csv",
        ["candidate", "exact_match_accuracy", "mean_absolute_error", "average_runtime_ms"],
        csv_rows,
    )
    save_text(destination / "tuning-results.md", _build_markdown_table(csv_rows))

    return {
        "source_profile": source_profile_name,
        "best_candidate": rankings[0]["candidate"] if rankings else None,
        "rankings": rankings,
    }


def build_candidate_profiles(
    source_profile_name: str, source_profile: dict[str, Any]
) -> list[tuple[str, dict[str, Any]]]:
    if source_profile["color_space"] == "rgb":
        return _build_rgb_candidates(source_profile_name, source_profile)
    if source_profile["color_space"] == "hsv":
        return _build_hsv_candidates(source_profile_name, source_profile)
    raise ValueError(f"Unsupported color space for tuning: {source_profile['color_space']}")


def _build_rgb_candidates(
    source_profile_name: str, source_profile: dict[str, Any]
) -> list[tuple[str, dict[str, Any]]]:
    candidates = []
    base_lower = list(source_profile["lower"])
    base_upper = list(source_profile["upper"])
    variants = {
        "base": (0, 0),
        "relaxed": (-20, 20),
        "strict": (10, -10),
        "lower-green-blue": (0, 25),
    }
    for suffix, (lower_delta, upper_delta) in variants.items():
        profile = deepcopy(source_profile)
        profile["lower"] = [
            _clamp_channel(base_lower[0] + lower_delta),
            _clamp_channel(base_lower[1]),
            _clamp_channel(base_lower[2]),
        ]
        profile["upper"] = [
            _clamp_channel(base_upper[0]),
            _clamp_channel(base_upper[1] + upper_delta),
            _clamp_channel(base_upper[2] + upper_delta),
        ]
        candidates.append((f"{source_profile_name}-{suffix}", profile))
    return candidates


def _build_hsv_candidates(
    source_profile_name: str, source_profile: dict[str, Any]
) -> list[tuple[str, dict[str, Any]]]:
    candidates = []
    variants = {
        "base": (0, 0),
        "low-light-friendly": (-20, -20),
        "strict": (20, 20),
        "saturation-relaxed": (-25, 0),
    }
    for suffix, (sat_delta, value_delta) in variants.items():
        profile = deepcopy(source_profile)
        for current_range in profile["ranges"]:
            current_range["lower"][1] = _clamp_channel(current_range["lower"][1] + sat_delta)
            current_range["lower"][2] = _clamp_channel(current_range["lower"][2] + value_delta)
        candidates.append((f"{source_profile_name}-{suffix}", profile))
    return candidates


def _clamp_channel(value: int) -> int:
    return max(0, min(255, value))


def _build_markdown_table(rows: list[dict[str, Any]]) -> str:
    header = "| Candidate | Exact Match Accuracy | Mean Absolute Error | Average Runtime (ms) |"
    divider = "| --- | ---: | ---: | ---: |"
    body = [
        "| "
        f"{row['candidate']} | {row['exact_match_accuracy']:.3f} | "
        f"{row['mean_absolute_error']:.3f} | {row['average_runtime_ms']:.4f} |"
        for row in rows
    ]
    return "\n".join([header, divider, *body]) + "\n"
