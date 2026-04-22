"""Connected-component extraction and counting."""

from __future__ import annotations

from collections import deque

import numpy as np


def count_connected_components(
    mask: np.ndarray, min_component_size: int = 1
) -> tuple[int, list[int]]:
    if mask.ndim != 2:
        raise ValueError("Connected-component counting expects a 2D mask.")

    visited = np.zeros(mask.shape, dtype=bool)
    component_sizes: list[int] = []
    rows, cols = mask.shape

    for row in range(rows):
        for col in range(cols):
            if not mask[row, col] or visited[row, col]:
                continue

            queue = deque([(row, col)])
            visited[row, col] = True
            size = 0

            while queue:
                current_row, current_col = queue.popleft()
                size += 1
                for next_row, next_col in _neighbors(current_row, current_col, rows, cols):
                    if not mask[next_row, next_col] or visited[next_row, next_col]:
                        continue
                    visited[next_row, next_col] = True
                    queue.append((next_row, next_col))

            if size >= min_component_size:
                component_sizes.append(size)

    return len(component_sizes), component_sizes


def _neighbors(row: int, col: int, rows: int, cols: int) -> list[tuple[int, int]]:
    return [
        (next_row, next_col)
        for next_row, next_col in ((row - 1, col), (row + 1, col), (row, col - 1), (row, col + 1))
        if 0 <= next_row < rows and 0 <= next_col < cols
    ]
