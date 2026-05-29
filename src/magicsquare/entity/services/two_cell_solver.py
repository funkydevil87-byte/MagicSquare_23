"""Domain service for attempting a two-cell magic square completion."""

from __future__ import annotations

from magicsquare.entity.services.magic_square_validator import MagicSquareValidator


class TwoCellSolver:
    """Try filling two blanks and validate the completed magic square."""

    def __init__(self) -> None:
        self._validator = MagicSquareValidator()

    def attempt(
        self,
        partial: list[list[int]],
        first_blank: tuple[int, int],
        second_blank: tuple[int, int],
        first_value: int,
        second_value: int,
    ) -> list[int] | None:
        """Return ``[r1,c1,n1,r2,c2,n2]`` when the pairing is valid, else ``None``."""
        completed = self._validator.complete_grid(
            partial,
            first_blank,
            second_blank,
            first_value,
            second_value,
        )
        if not self._validator.validate_complete(completed).valid:
            return None

        r1, c1 = first_blank
        r2, c2 = second_blank
        return [r1, c1, first_value, r2, c2, second_value]
