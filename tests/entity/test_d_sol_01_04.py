"""D-SOL-01~04 — SolvePartialMagicSquare / solution vector. Track B Control."""

from __future__ import annotations

import pytest

from magicsquare.control.solve_partial_magic_square import SolvePartialMagicSquare
from magicsquare.entity.exceptions import UnsolvableDomainError
from tests.entity.conftest import GRID_G2, GRID_G3, GRID_TD01


class TestDSol01StepA:
    """D-SOL-01 — TD-01 small-first success vector."""

    def test_d_sol_01_td01_step_a_vector(self) -> None:
        # Arrange
        solver = SolvePartialMagicSquare()

        # Act
        result = solver.execute(GRID_TD01)

        # Assert
        assert result == [1, 2, 3, 1, 4, 13]


class TestDSol02StepB:
    """D-SOL-02 — G2 reverse-only success."""

    def test_d_sol_02_g2_reverse_vector(self) -> None:
        # Arrange
        solver = SolvePartialMagicSquare()

        # Act
        result = solver.execute(GRID_G2)

        # Assert
        assert result == [1, 1, 16, 1, 2, 3]


class TestDSol03Unsolvable:
    """D-SOL-03 — G3 both combinations fail."""

    def test_d_sol_03_g3_unsolvable_domain_error(self) -> None:
        # Arrange
        solver = SolvePartialMagicSquare()

        # Act / Assert
        with pytest.raises(UnsolvableDomainError):
            solver.execute(GRID_G3)


class TestDSol04OutputShape:
    """D-SOL-04 — TD-01 output contract (len=6, 1-index)."""

    def test_d_sol_04_td01_output_length_and_indexing(self) -> None:
        # Arrange
        solver = SolvePartialMagicSquare()

        # Act
        result = solver.execute(GRID_TD01)

        # Assert
        assert len(result) == 6
        r1, c1, n1, r2, c2, n2 = result
        assert 1 <= r1 <= 4
        assert 1 <= c1 <= 4
        assert 1 <= r2 <= 4
        assert 1 <= c2 <= 4
        assert 1 <= n1 <= 16
        assert 1 <= n2 <= 16
        assert n1 != n2
