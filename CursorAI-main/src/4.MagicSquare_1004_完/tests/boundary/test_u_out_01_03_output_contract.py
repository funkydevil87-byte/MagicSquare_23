"""Report/09 Track A — U-OUT-01~03 output contract RED skeleton.

Success int[6] / 1-index / E006 mapping. Control mock 허용 (Dual-Track).
AC-FR05-01~03. Full assert는 Full RED 단계에서 추가.
"""

from __future__ import annotations

import pytest

from boundary.ui_boundary import UIBoundary
from control.solve_partial_magic_square import SolvePartialMagicSquare

# Report/02 G1 — 부분 격자, U-OUT Given
# grid_g1 = [[16,3,2,13],[5,0,11,8],[9,6,0,12],[4,15,14,1]]
# Control mock 반환: [2,2,7,3,3,10]


class TestSuccessOutputContract:
    """U-OUT-01, U-OUT-02 — 성공 envelope 및 int[6] 1-index."""

    def test_u_out_01_success_returns_int_six_tuple(self) -> None:
        """U-OUT-01, AC-FR05-01 — G1, type OK, data [2,2,7,3,3,10], len 6."""
        # U-OUT-01
        # Given
        grid_g1 = [[16, 3, 2, 13], [5, 0, 11, 8], [9, 6, 0, 12], [4, 15, 14, 1]]
        boundary = UIBoundary(solve_use_case=SolvePartialMagicSquare())

        # When
        result = boundary.solve(grid_g1)

        # Then
        assert result.type == "OK"
        assert result.data == [2, 2, 7, 3, 3, 10]
        assert len(result.data) == 6
        assert "error" not in result.model_dump()

    def test_u_out_02_success_coordinates_are_one_indexed(self) -> None:
        """U-OUT-02, AC-FR05-02 — r,c ∈ [1,4], UX-04."""
        # U-OUT-02
        # Given
        # mock_execute = MagicMock(spec=SolvePartialMagicSquare)
        # mock_execute.execute.return_value = [2, 2, 7, 3, 3, 10]
        # boundary = UIBoundary(solve_use_case=mock_execute)
        # When
        # result = boundary.solve(grid_g1)
        # Then — data[0],data[1],data[3],data[4] in [1,4]
        pytest.fail("RED: U-OUT-02 — 성공 좌표 1-index 범위")


class TestDomainFailureMapping:
    """U-OUT-03 — UnsolvableDomainError → E006."""

    def test_u_out_03_unsolvable_maps_to_e006(self) -> None:
        """U-OUT-03, AC-FR05-03 — mock UnsolvableDomainError → E006."""
        # U-OUT-03
        # Given
        # mock_execute = MagicMock(spec=SolvePartialMagicSquare)
        # mock_execute.execute.side_effect = UnsolvableDomainError(...)
        # boundary = UIBoundary(solve_use_case=mock_execute)
        # When
        # result = boundary.solve(grid_g1)
        # Then — type ERROR, code E006, message exact
        pytest.fail("RED: U-OUT-03 — Domain 무해 → E006 매핑")
