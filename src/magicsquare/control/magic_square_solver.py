"""Control-layer solver orchestration."""

from __future__ import annotations

from typing import Any

from magicsquare.control.exceptions import SolveUnsolvableError
from magicsquare.control.solve_partial_magic_square import SolvePartialMagicSquare
from magicsquare.entity.exceptions import UnsolvableDomainError


class MagicSquareSolver:
    """Orchestrates domain resolve for valid grids."""

    def __init__(self) -> None:
        self._solver = SolvePartialMagicSquare()

    def resolve(self, grid: Any) -> list[int]:
        """Run the partial magic square solve pipeline.

        Args:
            grid: Validated 4x4 partial grid.

        Returns:
            Solution vector ``[r1, c1, n1, r2, c2, n2]``.

        Raises:
            SolveUnsolvableError: When both solve attempts fail.
        """
        try:
            return self._solver.execute(grid)
        except UnsolvableDomainError as exc:
            raise SolveUnsolvableError from exc
