"""Report/09 Track B — D-SOL-01~04 two cell solver RED skeleton.

Step A/B 해결 및 출력 계약. Domain Mock 금지. AC-FR05-*.
"""

from __future__ import annotations

import pytest

from entity.services.two_cell_solver import TwoCellSolver

# Report/02 G1 — Step A 성공, 기대 [2,2,7,3,3,10]
# grid_g1 = [[16,3,2,13],[5,0,11,8],[9,6,0,12],[4,15,14,1]]

# Report/02 G3 — 무해
# grid_g3 = [[1,2,3,0],[5,6,0,8],[9,10,11,12],[13,14,15,16]]


class TestTwoCellSolverStepA:
    """D-SOL-01 — G1 Step A 성공."""

    def test_d_sol_01_g1_step_a_returns_solution(self) -> None:
        """D-SOL-01, I8 — G1 solution → [2,2,7,3,3,10]."""
        # D-SOL-01
        # Given
        solver = TwoCellSolver()
        grid = [[16, 3, 2, 13], [5, 0, 11, 8], [9, 6, 0, 12], [4, 15, 14, 1]]

        # When
        result = solver.solve(grid)

        # Then — Step B restores G0; PRD fixture label says Step A but placement
        # smaller→first, larger→second fails validation for this grid.
        assert result.values == [2, 2, 10, 3, 3, 7]


class TestTwoCellSolverStepB:
    """D-SOL-02 — G2 Step B만 성공 [TBD]."""

    def test_d_sol_02_g2_step_b_only_returns_solution(self) -> None:
        """D-SOL-02, I9 — G2 Step B fallback (G2 TBD)."""
        # D-SOL-02
        # Given
        # solver = TwoCellSolver()
        # grid = grid_g2  # Report/02 placeholder — TBD
        # When
        # result = solver.solve(grid)
        # Then — Step B 배치 [r1,c1,n1,r2,c2,n2]
        pytest.fail("RED: D-SOL-02 — G2 TBD")


class TestTwoCellSolverUnsolvable:
    """D-SOL-03 — G3 무해 → UnsolvableDomainError."""

    def test_d_sol_03_g3_raises_unsolvable(self) -> None:
        """D-SOL-03, I10 — G3 → UnsolvableDomainError."""
        # D-SOL-03
        # Given
        # solver = TwoCellSolver()
        # grid = grid_g3
        # When / Then
        # with pytest.raises(UnsolvableDomainError):
        #     solver.solve(grid)
        pytest.fail("RED: D-SOL-03 — G3 무해 → UnsolvableDomainError")


class TestTwoCellSolverOutputContract:
    """D-SOL-04 — 반환 길이 6·좌표 1-index."""

    def test_d_sol_04_g1_result_length_and_one_index(self) -> None:
        """D-SOL-04, I8 — G1 len==6, 좌표 ∈ [1,4]."""
        # D-SOL-04
        # Given
        # solver = TwoCellSolver()
        # grid = grid_g1
        # When
        # result = solver.solve(grid)
        # Then — len(result)==6; r,c ∈ [1,4]
        pytest.fail("RED: D-SOL-04 — 반환 길이 6·좌표 1-index")
