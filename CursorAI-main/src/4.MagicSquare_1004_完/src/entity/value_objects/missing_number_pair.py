"""Pair of missing numbers in ascending order."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class MissingNumberPair:
    """Two missing values from the set {1..16} not present in the grid.

    Attributes:
        smaller: The smaller missing value.
        larger: The larger missing value.
    """

    smaller: int
    larger: int
