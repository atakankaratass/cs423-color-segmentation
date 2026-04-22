"""Smoke-test the repository evaluation flow on the bundled sample dataset."""

from __future__ import annotations

import os
import subprocess
import sys
import tempfile
from pathlib import Path


def main() -> int:
    repo_root = Path(__file__).resolve().parent.parent
    env = os.environ.copy()
    src_path = str(repo_root / "src")
    existing_pythonpath = env.get("PYTHONPATH")
    env["PYTHONPATH"] = src_path if not existing_pythonpath else f"{src_path}:{existing_pythonpath}"
    with tempfile.TemporaryDirectory() as temp_dir:
        output_path = Path(temp_dir) / "smoke-results.json"
        command = [
            sys.executable,
            "-m",
            "cs423_segmentation",
            "run-experiments",
            "--metadata",
            "data/sample/metadata/dataset.json",
            "--output",
            str(output_path),
        ]
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
        if not output_path.exists():
            sys.stderr.write("Expected evaluation output file was not produced.\n")
            return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
