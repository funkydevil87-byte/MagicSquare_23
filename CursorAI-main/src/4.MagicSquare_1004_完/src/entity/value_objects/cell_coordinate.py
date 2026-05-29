"""1-index cell coordinate value object."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class CellCoordinate:
    """Immutable 1-index grid position.

    Attributes:
        row: Row index from 1 to grid size.
        col: Column index from 1 to grid size.
    """

    row: int
    col: int
