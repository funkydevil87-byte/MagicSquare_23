"""Domain numeric constants SSOT for Magic Square 4×4."""

from __future__ import annotations


class GridSize:
    """Fixed row and column count for the partial magic square grid."""

    VALUE = 4


class MagicConstant:
    """Target sum for each row, column, and diagonal in a complete 4×4 grid."""

    VALUE = 34


class CellValueRange:
    """Inclusive bounds for non-empty cell values."""

    MIN = 1
    MAX = 16
