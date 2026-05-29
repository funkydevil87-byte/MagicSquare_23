"""SC-CTL-001 — SolvePartialMagicSquare use-case orchestration RED/GREEN."""

from __future__ import annotations

from control.solve_partial_magic_square import SolvePartialMagicSquare

# Report/02 G1 — Step A output contract [2,2,7,3,3,10]
# grid_g1 = [[16,3,2,13],[5,0,11,8],[9,6,0,12],[4,15,14,1]]


class TestSolvePartialMagicSquareOrchestration:
    """Control — locate → find → solve pipeline for validated G1."""

    def test_sc_ctl_001_g1_resolve_returns_int_six(self) -> None:
        """SC-CTL-001 — G1 resolve() → [2,2,7,3,3,10] via domain services."""
        # SC-CTL-001
        # Given
        use_case = SolvePartialMagicSquare()
        grid = [[16, 3, 2, 13], [5, 0, 11, 8], [9, 6, 0, 12], [4, 15, 14, 1]]

        # When
        result = use_case.resolve(grid)

        # Then
        assert result == [2, 2, 7, 3, 3, 10]
