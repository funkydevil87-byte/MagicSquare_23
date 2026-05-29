"""Report/09 Track A — U-IN-04~08 input validation RED skeleton.

PRD §12.3 E002~E005 Failure envelope. Domain execute 0회 (U-FLOW-02 확장 대상).
AC-FR01-04~06. Full assert는 Full RED 단계에서 추가.
"""

from __future__ import annotations

import pytest

from boundary.input_validator import InputValidator

# Report/02 G0 — 완전 격자 (0 없음), U-IN-04 Given
# grid_g0 = [[16,3,2,13],[5,10,11,8],[9,6,7,12],[4,15,14,1]]


class TestEmptyCountValidation:
    """U-IN-04, U-IN-05 — 빈칸(0) 개수 ≠ 2 → E002."""

    def test_u_in_04_zero_empty_cells_returns_e002(self) -> None:
        """U-IN-04, AC-FR01-04 — G0 완전 격자, count(0)==0 → E002."""
        # U-IN-04
        # Given
        validator = InputValidator()
        matrix = [[16, 3, 2, 13], [5, 10, 11, 8], [9, 6, 7, 12], [4, 15, 14, 1]]

        # When
        result = validator.validate(matrix)

        # Then
        assert result.type == "ERROR"
        assert result.error.code == "E002"
        assert (
            result.error.message
            == "INVALID_EMPTY_COUNT: expected exactly 2 empty cells (0)"
        )

    def test_u_in_05_three_empty_cells_returns_e002(self) -> None:
        """U-IN-05, AC-FR01-04 — 4×4, 0 세 개 → E002."""
        # U-IN-05
        # Given
        validator = InputValidator()
        matrix = [[0, 3, 2, 13], [5, 0, 11, 8], [9, 6, 0, 12], [4, 15, 14, 1]]

        # When
        result = validator.validate(matrix)

        # Then
        assert result.type == "ERROR"
        assert result.error.code == "E002"
        assert (
            result.error.message
            == "INVALID_EMPTY_COUNT: expected exactly 2 empty cells (0)"
        )


class TestValueRangeValidation:
    """U-IN-06, U-IN-07 — 값 ∉ {0}∪{1..16} → E004."""

    def test_u_in_06_cell_minus_one_returns_e004(self) -> None:
        """U-IN-06, AC-FR01-05 — 셀 -1, 0 두 개 → E004."""
        # U-IN-06
        # Given
        # validator = InputValidator()
        # matrix = [[16,3,2,13],[-1,0,11,8],[9,6,0,12],[4,15,14,1]]
        # When
        # result = validator.validate(matrix)
        # Then — E004, message exact, Domain 0회
        pytest.fail("RED: U-IN-06 — 셀 -1 → E004")

    def test_u_in_07_cell_seventeen_returns_e004(self) -> None:
        """U-IN-07, AC-FR01-05 — 셀 17, 0 두 개 → E004."""
        # U-IN-07
        # Given
        # validator = InputValidator()
        # matrix = [[16,3,2,13],[5,0,11,8],[9,6,0,12],[4,15,14,17]]
        # When
        # result = validator.validate(matrix)
        # Then — E004, message exact, Domain 0회
        pytest.fail("RED: U-IN-07 — 셀 17 → E004")


class TestDuplicateValidation:
    """U-IN-08 — non-zero 중복 → E005."""

    def test_u_in_08_duplicate_non_zero_returns_e005(self) -> None:
        """U-IN-08, AC-FR01-06 — 5 중복, 0 두 개 → E005."""
        # U-IN-08
        # Given
        # validator = InputValidator()
        # matrix = [[16,3,2,13],[5,0,11,8],[9,6,0,12],[4,15,14,5]]
        # When
        # result = validator.validate(matrix)
        # Then — E005, message exact, Domain 0회
        pytest.fail("RED: U-IN-08 — non-zero 5 중복 → E005")
