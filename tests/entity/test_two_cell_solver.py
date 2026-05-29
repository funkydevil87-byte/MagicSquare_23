"""D-SOL — TwoCellSolver domain attempt service."""

from __future__ import annotations

import copy

from magicsquare.entity.services.two_cell_solver import TwoCellSolver
from tests.entity.conftest import GRID_G2, GRID_G3, GRID_TD01


class TestTwoCellSolverAttemptOne:
    """D-SOL-01 — TD-01 small-first valid pairing."""

    def test_d_sol_01_td01_small_first_returns_vector(self) -> None:
        solver = TwoCellSolver()
        grid = copy.deepcopy(GRID_TD01)
        first_blank = (1, 2)
        second_blank = (1, 4)

        result = solver.attempt(grid, first_blank, second_blank, 3, 13)

        assert result == [1, 2, 3, 1, 4, 13]


class TestTwoCellSolverAttemptTwo:
    """D-SOL-02 — G2 reverse-only valid pairing."""

    def test_d_sol_02_g2_large_small_returns_vector(self) -> None:
        solver = TwoCellSolver()
        grid = copy.deepcopy(GRID_G2)
        first_blank = (1, 1)
        second_blank = (1, 2)

        result = solver.attempt(grid, first_blank, second_blank, 16, 3)

        assert result == [1, 1, 16, 1, 2, 3]

    def test_d_sol_02_g2_small_large_returns_none(self) -> None:
        solver = TwoCellSolver()
        grid = copy.deepcopy(GRID_G2)
        first_blank = (1, 1)
        second_blank = (1, 2)

        result = solver.attempt(grid, first_blank, second_blank, 3, 16)

        assert result is None


class TestTwoCellSolverUnsolvable:
    """D-SOL-03 — G3 both pairings invalid."""

    def test_d_sol_03_g3_both_pairings_return_none(self) -> None:
        solver = TwoCellSolver()
        grid = copy.deepcopy(GRID_G3)
        first_blank = (2, 2)
        second_blank = (3, 3)

        assert solver.attempt(grid, first_blank, second_blank, 7, 10) is None
        assert solver.attempt(grid, first_blank, second_blank, 10, 7) is None


class TestTwoCellSolverOutputShape:
    """D-SOL-04 — vector contract (len=6, 1-index)."""

    def test_d_sol_04_td01_output_length_and_indexing(self) -> None:
        solver = TwoCellSolver()
        grid = copy.deepcopy(GRID_TD01)
        first_blank = (1, 2)
        second_blank = (1, 4)

        result = solver.attempt(grid, first_blank, second_blank, 3, 13)

        assert result is not None
        assert len(result) == 6
        r1, c1, n1, r2, c2, n2 = result
        assert 1 <= r1 <= 4
        assert 1 <= c1 <= 4
        assert 1 <= r2 <= 4
        assert 1 <= c2 <= 4
        assert 1 <= n1 <= 16
        assert 1 <= n2 <= 16
        assert n1 != n2
