"""Connected-component extraction and counting."""

from __future__ import annotations

from collections import deque

import numpy as np


def count_connected_components(
    mask: np.ndarray, min_component_size: int = 1
) -> tuple[int, list[int]]:
    components = extract_components(mask, min_component_size=min_component_size)
    return len(components), [int(component.sum()) for component in components]


def extract_components(mask: np.ndarray, min_component_size: int = 1) -> list[np.ndarray]:
    if mask.ndim != 2:
        raise ValueError("Connected-component counting expects a 2D mask.")

    visited = np.zeros(mask.shape, dtype=bool)
    components: list[np.ndarray] = []
    rows, cols = mask.shape

    for row in range(rows):
        for col in range(cols):
            if not mask[row, col] or visited[row, col]:
                continue

            queue = deque([(row, col)])
            visited[row, col] = True
            component_mask = np.zeros(mask.shape, dtype=bool)

            while queue:
                current_row, current_col = queue.popleft()
                component_mask[current_row, current_col] = True
                for next_row, next_col in _neighbors(current_row, current_col, rows, cols):
                    if not mask[next_row, next_col] or visited[next_row, next_col]:
                        continue
                    visited[next_row, next_col] = True
                    queue.append((next_row, next_col))

            if int(component_mask.sum()) >= min_component_size:
                components.append(component_mask)

    return components


def _neighbors(row: int, col: int, rows: int, cols: int) -> list[tuple[int, int]]:
    return [
        (next_row, next_col)
        for next_row, next_col in ((row - 1, col), (row + 1, col), (row, col - 1), (row, col + 1))
        if 0 <= next_row < rows and 0 <= next_col < cols
    ]
