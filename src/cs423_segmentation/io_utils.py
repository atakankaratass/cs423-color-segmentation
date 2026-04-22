"""Repository-safe image and JSON I/O helpers."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Union

import numpy as np
from PIL import Image


def load_image(path: Union[str, Path]) -> np.ndarray:
    image = Image.open(path).convert("RGB")
    return np.asarray(image, dtype=np.uint8)


def save_json(path: Union[str, Path], payload: Any) -> None:
    destination = Path(path)
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(json.dumps(payload, indent=2), encoding="utf-8")


def load_json(path: Union[str, Path]) -> Any:
    return json.loads(Path(path).read_text(encoding="utf-8"))
