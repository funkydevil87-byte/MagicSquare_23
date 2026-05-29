"""Shared grid fixtures (G0~G3) for Track B tests."""

from __future__ import annotations

import copy

# G0 — complete 4×4 magic square (M=34)
GRID_G0: list[list[int]] = [
    [16, 3, 2, 13],
    [5, 10, 11, 8],
    [9, 6, 7, 12],
    [4, 15, 14, 1],
]

# G1 — partial grid, blanks at (2,2) and (3,3), missing {7, 10}
GRID_G1: list[list[int]] = [
    [16, 3, 2, 13],
    [5, 0, 11, 8],
    [9, 6, 0, 12],
    [4, 15, 14, 1],
]

# G2 / TD-02 — reverse-only success; blanks at (1,1) and (1,2)
GRID_G2: list[list[int]] = [
    [0, 0, 2, 13],
    [5, 10, 11, 8],
    [9, 6, 7, 12],
    [4, 15, 14, 1],
]

# TD-01 — small-first-only success; blanks at (1,2) and (1,4)
GRID_TD01: list[list[int]] = [
    [16, 0, 2, 0],
    [5, 10, 11, 8],
    [9, 6, 7, 12],
    [4, 15, 14, 1],
]

# G3 — both combinations fail (ES-05)
GRID_G3: list[list[int]] = [
    [1, 2, 3, 4],
    [5, 6, 0, 8],
    [9, 0, 11, 12],
    [13, 14, 15, 16],
]


def disturbed_row_one(grid: list[list[int]]) -> list[list[int]]:
    """Return G0 with row 1 sum broken."""
    disturbed = copy.deepcopy(grid)
    disturbed[0][0] = 15
    return disturbed


def disturbed_col_one(grid: list[list[int]]) -> list[list[int]]:
    """Return G0 with column 1 sum broken."""
    disturbed = copy.deepcopy(grid)
    disturbed[1][0] = 4
    return disturbed


def disturbed_diagonal(grid: list[list[int]]) -> list[list[int]]:
    """Return G0 with main diagonal sum broken."""
    disturbed = copy.deepcopy(grid)
    disturbed[1][1] = 9
    return disturbed


def duplicate_complete_grid(grid: list[list[int]]) -> list[list[int]]:
    """Return a full grid with a duplicated non-zero value."""
    disturbed = copy.deepcopy(grid)
    disturbed[3][3] = 3
    return disturbed


def zero_on_complete_grid(grid: list[list[int]]) -> list[list[int]]:
    """Return a labeled-complete grid that still contains a blank."""
    disturbed = copy.deepcopy(grid)
    disturbed[0][0] = 0
    return disturbed
