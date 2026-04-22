"""Command-line entrypoint for the segmentation and evaluation workflows."""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import List, Optional

from cs423_segmentation.evaluation import evaluate_dataset, run_experiments
from cs423_segmentation.reporting import generate_report


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

    parser.error(f"Unsupported command: {args.command}")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
