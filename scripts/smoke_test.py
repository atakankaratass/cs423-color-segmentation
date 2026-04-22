"""Smoke-test the repository CLI entrypoint."""

from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path


def main() -> int:
    repo_root = Path(__file__).resolve().parent.parent
    env = os.environ.copy()
    src_path = str(repo_root / "src")
    existing_pythonpath = env.get("PYTHONPATH")
    env["PYTHONPATH"] = src_path if not existing_pythonpath else f"{src_path}:{existing_pythonpath}"
    command = [sys.executable, "-m", "cs423_segmentation", "--help"]
    completed = subprocess.run(
        command,
        cwd=repo_root,
        check=False,
        capture_output=True,
        text=True,
        env=env,
    )
    if completed.returncode != 0:
        sys.stderr.write(completed.stderr)
        return completed.returncode
    if "CS423 color segmentation CLI" not in completed.stdout:
        sys.stderr.write("Expected CLI help text was not produced.\n")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
