"""Command-line entrypoint for the segmentation and evaluation workflows."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import List, Optional

from cs423_segmentation.dataset import validate_dataset
from cs423_segmentation.evaluation import evaluate_dataset, run_experiments
from cs423_segmentation.reporting import build_report_bundle, generate_report
from cs423_segmentation.tuning import tune_profile


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="CS423 color segmentation CLI")
    subparsers = parser.add_subparsers(dest="command", required=True)

    evaluate_parser = subparsers.add_parser("evaluate", help="Run a dataset evaluation profile.")
    evaluate_parser.add_argument(
        "--metadata", required=True, help="Path to the dataset metadata JSON file."
    )
    evaluate_parser.add_argument(
        "--profile", required=True, help="Profile name defined in the metadata file."
    )
    evaluate_parser.add_argument(
        "--output", required=True, help="Where to write the evaluation summary JSON."
    )

    experiments_parser = subparsers.add_parser(
        "run-experiments", help="Run all configured profiles and write a combined summary."
    )
    experiments_parser.add_argument(
        "--metadata", required=True, help="Path to the dataset metadata JSON file."
    )
    experiments_parser.add_argument(
        "--output", required=True, help="Where to write the combined experiment summary JSON."
    )

    report_parser = subparsers.add_parser(
        "generate-report", help="Write JSON, CSV, and visualization artifacts for all profiles."
    )
    report_parser.add_argument(
        "--metadata", required=True, help="Path to the dataset metadata JSON file."
    )
    report_parser.add_argument(
        "--output-dir", required=True, help="Directory where report artifacts will be written."
    )

    validate_parser = subparsers.add_parser(
        "validate-dataset", help="Validate dataset metadata labels, IDs, and file paths."
    )
    validate_parser.add_argument(
        "--metadata", required=True, help="Path to the dataset metadata JSON file."
    )

    tuning_parser = subparsers.add_parser(
        "tune-profile", help="Evaluate small candidate variations around an existing profile."
    )
    tuning_parser.add_argument(
        "--metadata", required=True, help="Path to the dataset metadata JSON file."
    )
    tuning_parser.add_argument(
        "--profile", required=True, help="Existing profile name to tune around."
    )
    tuning_parser.add_argument(
        "--output-dir", required=True, help="Directory where tuning artifacts will be written."
    )

    bundle_parser = subparsers.add_parser(
        "build-bundle",
        help="Validate dataset, generate structured report outputs, and optionally tune profiles.",
    )
    bundle_parser.add_argument(
        "--metadata", required=True, help="Path to the dataset metadata JSON file."
    )
    bundle_parser.add_argument(
        "--output-dir", required=True, help="Directory where bundle artifacts will be written."
    )
    bundle_parser.add_argument(
        "--skip-tuning", action="store_true", help="Skip per-profile tuning artifacts."
    )

    return parser


def main(argv: Optional[List[str]] = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.command == "evaluate":
        evaluate_dataset(Path(args.metadata), args.profile, Path(args.output))
        return 0
    if args.command == "run-experiments":
        run_experiments(Path(args.metadata), Path(args.output))
        return 0
    if args.command == "generate-report":
        generate_report(Path(args.metadata), Path(args.output_dir))
        return 0
    if args.command == "validate-dataset":
        result = validate_dataset(Path(args.metadata))
        if result["is_valid"]:
            return 0
        for error in result["errors"]:
            print(error)
        return 1
    if args.command == "tune-profile":
        tune_profile(Path(args.metadata), args.profile, Path(args.output_dir))
        return 0
    if args.command == "build-bundle":
        try:
            build_report_bundle(
                Path(args.metadata), Path(args.output_dir), include_tuning=not args.skip_tuning
            )
        except (FileNotFoundError, ValueError) as error:
            print(error, file=sys.stderr)
            return 1
        return 0

    parser.error(f"Unsupported command: {args.command}")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
