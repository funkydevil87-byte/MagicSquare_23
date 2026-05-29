"""Six-element solution tuple for two-cell magic square completion."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class SolutionResult:
    """Domain solution as ``[r1, c1, n1, r2, c2, n2]`` (1-index).

    Attributes:
        values: Six integers describing both fill coordinates and numbers.
    """

    values: list[int]
