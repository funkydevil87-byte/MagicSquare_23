"""Use case orchestrator for partial magic square solving."""

from __future__ import annotations

from entity.services.empty_cell_locator import EmptyCellLocator
from entity.services.missing_number_finder import MissingNumberFinder
from entity.services.two_cell_solver import TwoCellSolver


class SolvePartialMagicSquare:
    """Orchestrates locate → find → solve for a validated 4×4 grid."""

    def __init__(
        self,
        empty_cell_locator: EmptyCellLocator | None = None,
        missing_number_finder: MissingNumberFinder | None = None,
        two_cell_solver: TwoCellSolver | None = None,
    ) -> None:
        """Initialize use case with injectable domain services.

        Args:
            empty_cell_locator: Locates empty cells in row-major order.
            missing_number_finder: Finds the two missing values from {1..16}.
            two_cell_solver: Attempts Step A/B completion and validation.
        """
        self._empty_cell_locator = empty_cell_locator or EmptyCellLocator()
        self._missing_number_finder = missing_number_finder or MissingNumberFinder()
        self._two_cell_solver = two_cell_solver or TwoCellSolver()

    def resolve(self, grid: list[list[int]]) -> list[int]:
        """Run locate → find → solve and return ``int[6]`` for a valid grid.

        Args:
            grid: Validated 4×4 integer matrix with exactly two empty cells.

        Returns:
            Six-element result ``[r1, c1, n1, r2, c2, n2]`` (1-index).

        Raises:
            UnsolvableDomainError: When the domain solver finds no completion.
        """
        empty_cells = self._empty_cell_locator.locate(grid)
        missing_numbers = self._missing_number_finder.find(grid)
        self._two_cell_solver.solve(grid)
        return [
            empty_cells.first.row,
            empty_cells.first.col,
            missing_numbers.smaller,
            empty_cells.second.row,
            empty_cells.second.col,
            missing_numbers.larger,
        ]
