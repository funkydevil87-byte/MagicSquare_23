"""Golden Master input scenarios for Magic Square Solver (GM-1)."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class GoldenMasterScenario:
    """Single scenario definition for golden master capture.

    Attributes:
        name: Section key used in ``golden_master_expected.txt``.
        grid: 4×4 integer matrix passed to ``UIBoundary.solve``.
        description: Human-readable note for design docs.
    """

    name: str
    grid: list[list[int]]
    description: str


# Report/05 §9 G2 — Step B-only success at Domain; UIBoundary int[6] output
_GRID_NORMAL_SUCCESS = [
    [16, 2, 3, 13],
    [5, 11, 10, 8],
    [9, 7, 0, 12],
    [4, 14, 15, 0],
]

# Report/02 G1 — alternate success path; UIBoundary int[6] output
_GRID_REVERSE_SUCCESS = [
    [16, 3, 2, 13],
    [5, 0, 11, 8],
    [9, 6, 0, 12],
    [4, 15, 14, 1],
]

# Report/02 G0 — zero empty cells → E002
_GRID_INVALID_BLANK_COUNT = [
    [16, 3, 2, 13],
    [5, 10, 11, 8],
    [9, 6, 7, 12],
    [4, 15, 14, 1],
]

# U-IN-08 — duplicate non-zero value → E005
_GRID_DUPLICATE_NUMBER = [
    [16, 3, 2, 13],
    [5, 0, 11, 8],
    [9, 6, 0, 12],
    [4, 15, 14, 5],
]

# Report/02 G3 — both Step A/B invalid → E006 (Domain contract)
_GRID_NO_VALID_SOLUTION = [
    [1, 2, 3, 0],
    [5, 6, 0, 8],
    [9, 10, 11, 12],
    [13, 14, 15, 16],
]

GOLDEN_MASTER_SCENARIOS: tuple[GoldenMasterScenario, ...] = (
    GoldenMasterScenario(
        name="normal_success",
        grid=_GRID_NORMAL_SUCCESS,
        description="Valid partial grid — successful solve (G2 fixture)",
    ),
    GoldenMasterScenario(
        name="reverse_success",
        grid=_GRID_REVERSE_SUCCESS,
        description="Valid partial grid — alternate success path (G1 fixture)",
    ),
    GoldenMasterScenario(
        name="invalid_blank_count",
        grid=_GRID_INVALID_BLANK_COUNT,
        description="Complete grid with zero blanks — E002",
    ),
    GoldenMasterScenario(
        name="duplicate_number",
        grid=_GRID_DUPLICATE_NUMBER,
        description="Duplicate non-zero value — E005",
    ),
    GoldenMasterScenario(
        name="no_valid_solution",
        grid=_GRID_NO_VALID_SOLUTION,
        description="Both combinations invalid — E006",
    ),
)
