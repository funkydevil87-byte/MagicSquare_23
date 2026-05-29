"""Report/09 Track A — U-FLOW-02 Domain isolation RED skeleton (확장).

invalid 입력 시 SolvePartialMagicSquare.execute 0회. Control mock/spy 허용.
U-IN-04~08 각 invalid 케이스 확장. AC-FR01-08, BR-05.
"""

from __future__ import annotations

import pytest

from boundary.ui_boundary import UIBoundary
from control.solve_partial_magic_square import SolvePartialMagicSquare

# Report/02 G0 — 완전 격자 (0 없음), U-IN-04 Given
# grid_g0 = [[16,3,2,13],[5,10,11,8],[9,6,7,12],[4,15,14,1]]


class TestDomainIsolationOnInvalidInput:
    """U-FLOW-02 — invalid 입력 시 execute 0회, Failure 반환."""

    def test_u_flow_02_size_violation_execute_never_called(self) -> None:
        """U-FLOW-02, AC-FR01-08 — 3×4 size 위반 → execute 0회."""
        # U-FLOW-02
        # Given
        # mock_execute = MagicMock(spec=SolvePartialMagicSquare)
        # boundary = UIBoundary(solve_use_case=mock_execute)
        # matrix = [[1,2,3,4],[5,6,7,8],[9,10,11,12]]
        # When
        # result = boundary.solve(matrix)
        # Then — execute.call_count == 0, Failure 반환
        pytest.fail("RED: U-FLOW-02 — 3×4 size 위반 → execute 0회")

    def test_u_flow_02_u_in_04_zero_empty_execute_never_called(self) -> None:
        """U-FLOW-02 확장, U-IN-04 — G0 빈칸 0개 → execute 0회."""
        # U-FLOW-02 / U-IN-04
        # Given
        # mock_execute = MagicMock(spec=SolvePartialMagicSquare)
        # boundary = UIBoundary(solve_use_case=mock_execute)
        # matrix = grid_g0
        # When
        # result = boundary.solve(matrix)
        # Then — execute.call_count == 0, E002 Failure
        pytest.fail("RED: U-FLOW-02 — U-IN-04 빈칸 0개 → execute 0회")

    def test_u_flow_02_u_in_05_three_empty_execute_never_called(self) -> None:
        """U-FLOW-02 확장, U-IN-05 — 빈칸 3개 → execute 0회."""
        # U-FLOW-02 / U-IN-05
        # Given
        # mock_execute = MagicMock(spec=SolvePartialMagicSquare)
        # boundary = UIBoundary(solve_use_case=mock_execute)
        # matrix = [[0,3,2,13],[5,0,11,8],[9,6,0,12],[4,15,14,1]]
        # When
        # result = boundary.solve(matrix)
        # Then — execute.call_count == 0, E002 Failure
        pytest.fail("RED: U-FLOW-02 — U-IN-05 빈칸 3개 → execute 0회")

    def test_u_flow_02_u_in_06_minus_one_execute_never_called(self) -> None:
        """U-FLOW-02 확장, U-IN-06 — 셀 -1 → execute 0회."""
        # U-FLOW-02 / U-IN-06
        # Given
        # mock_execute = MagicMock(spec=SolvePartialMagicSquare)
        # boundary = UIBoundary(solve_use_case=mock_execute)
        # matrix = [[16,3,2,13],[-1,0,11,8],[9,6,0,12],[4,15,14,1]]
        # When
        # result = boundary.solve(matrix)
        # Then — execute.call_count == 0, E004 Failure
        pytest.fail("RED: U-FLOW-02 — U-IN-06 셀 -1 → execute 0회")

    def test_u_flow_02_u_in_07_seventeen_execute_never_called(self) -> None:
        """U-FLOW-02 확장, U-IN-07 — 셀 17 → execute 0회."""
        # U-FLOW-02 / U-IN-07
        # Given
        # mock_execute = MagicMock(spec=SolvePartialMagicSquare)
        # boundary = UIBoundary(solve_use_case=mock_execute)
        # matrix = [[16,3,2,13],[5,0,11,8],[9,6,0,12],[4,15,14,17]]
        # When
        # result = boundary.solve(matrix)
        # Then — execute.call_count == 0, E004 Failure
        pytest.fail("RED: U-FLOW-02 — U-IN-07 셀 17 → execute 0회")

    def test_u_flow_02_u_in_08_duplicate_execute_never_called(self) -> None:
        """U-FLOW-02 확장, U-IN-08 — non-zero 5 중복 → execute 0회."""
        # U-FLOW-02 / U-IN-08
        # Given
        # mock_execute = MagicMock(spec=SolvePartialMagicSquare)
        # boundary = UIBoundary(solve_use_case=mock_execute)
        # matrix = [[16,3,2,13],[5,0,11,8],[9,6,0,12],[4,15,14,5]]
        # When
        # result = boundary.solve(matrix)
        # Then — execute.call_count == 0, E005 Failure
        pytest.fail("RED: U-FLOW-02 — U-IN-08 non-zero 5 중복 → execute 0회")
