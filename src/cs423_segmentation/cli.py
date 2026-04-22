"""Command-line entrypoint for the project scaffold."""

from __future__ import annotations

import argparse


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="CS423 color segmentation CLI")
    parser.add_argument(
        "--mode",
        default="scaffold",
        choices=["scaffold"],
        help="Temporary scaffold mode until the image-processing pipeline is added.",
    )
    return parser


def main() -> int:
    parser = build_parser()
    parser.parse_args()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
