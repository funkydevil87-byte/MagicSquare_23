"""Report/09 Track B — D-VAL-01~06 magic square validator RED skeleton.

완전 격자 I1~I5 검증. Domain Mock 금지. AC-FR04-*.
"""

from __future__ import annotations

import pytest

from entity.services.magic_square_validator import MagicSquareValidator

# Report/02 G0 — 완전 유효 마방jin
# grid_g0 = [[16,3,2,13],[5,10,11,8],[9,6,7,12],[4,15,14,1]]


class TestMagicSquareValidatorComplete:
    """D-VAL-01 — G0 완전 격자 → true."""

    def test_d_val_01_g0_complete_grid_returns_true(self) -> None:
        """D-VAL-01, I1~I5 — G0 is_valid_complete → True."""
        # D-VAL-01
        # Given
        validator = MagicSquareValidator()
        grid = [[16, 3, 2, 13], [5, 10, 11, 8], [9, 6, 7, 12], [4, 15, 14, 1]]

        # When
        result = validator.is_valid_complete(grid)

        # Then
        assert result is True


class TestMagicSquareValidatorRowSum:
    """D-VAL-02 — 행 합 불일치 → false."""

    def test_d_val_02_row_sum_mismatch_returns_false(self) -> None:
        """D-VAL-02, I1 — G0 (1,4)=99 대체 → False."""
        # D-VAL-02
        # Given
        # validator = MagicSquareValidator()
        # modified = copy grid_g0; modified[0][3] = 99
        # When
        # result = validator.is_valid_complete(modified)
        # Then — False
        pytest.fail("RED: D-VAL-02 — 행 합 불일치 → false")


class TestMagicSquareValidatorColSum:
    """D-VAL-03 — 열 합 불일치 → false."""

    def test_d_val_03_col_sum_mismatch_returns_false(self) -> None:
        """D-VAL-03, I2 — G0 열1 합 깨짐 → False."""
        # D-VAL-03
        # Given
        # validator = MagicSquareValidator()
        # modified = copy grid_g0; 열1 합 깨짐
        # When
        # result = validator.is_valid_complete(modified)
        # Then — False
        pytest.fail("RED: D-VAL-03 — 열 합 불일치 → false")


class TestMagicSquareValidatorDiagonal:
    """D-VAL-04 — 대각 불일치 → false."""

    def test_d_val_04_diagonal_mismatch_returns_false(self) -> None:
        """D-VAL-04, I3 — G0 대각 교환 등 → False."""
        # D-VAL-04
        # Given
        # validator = MagicSquareValidator()
        # modified = copy grid_g0; 대각 교환
        # When
        # result = validator.is_valid_complete(modified)
        # Then — False
        pytest.fail("RED: D-VAL-04 — 대각 불일치 → false")


class TestMagicSquareValidatorDuplicate:
    """D-VAL-05 — 1~16 중복 → false."""

    def test_d_val_05_duplicate_values_returns_false(self) -> None:
        """D-VAL-05, I4 — G0 값 중복 유발 → False."""
        # D-VAL-05
        # Given
        # validator = MagicSquareValidator()
        # modified = copy grid_g0; 값 중복 유발
        # When
        # result = validator.is_valid_complete(modified)
        # Then — False
        pytest.fail("RED: D-VAL-05 — 1~16 중복 → false")


class TestMagicSquareValidatorZeroCell:
    """D-VAL-06 — 0 포함 → false."""

    def test_d_val_06_zero_cell_returns_false(self) -> None:
        """D-VAL-06, I4 — G0 + 0 1개 → False."""
        # D-VAL-06
        # Given
        # validator = MagicSquareValidator()
        # grid_with_zero = copy grid_g0; 0 1개 삽입
        # When
        # result = validator.is_valid_complete(grid_with_zero)
        # Then — False
        pytest.fail("RED: D-VAL-06 — 0 포함 → false")
