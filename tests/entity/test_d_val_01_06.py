"""D-VAL-01~06 — MagicSquareValidator. Track B Entity."""

from __future__ import annotations

from magicsquare.entity.services.magic_square_validator import MagicSquareValidator
from tests.entity.conftest import (
    GRID_G0,
    duplicate_complete_grid,
    disturbed_col_one,
    disturbed_diagonal,
    disturbed_row_one,
    zero_on_complete_grid,
)


class TestDVal01CompleteGrid:
    """D-VAL-01 — G0 complete grid is valid with M=34."""

    def test_d_val_01_g0_complete_grid_valid_magic_constant(self) -> None:
        # Arrange
        validator = MagicSquareValidator()

        # Act
        result = validator.validate_complete(GRID_G0)

        # Assert
        assert result.valid is True


class TestDVal02RowDisturbance:
    """D-VAL-02 — G0 row 1 disturbed → invalid."""

    def test_d_val_02_g0_row_one_disturbed_invalid(self) -> None:
        # Arrange
        validator = MagicSquareValidator()
        disturbed = disturbed_row_one(GRID_G0)

        # Act
        result = validator.validate_complete(disturbed)

        # Assert
        assert result.valid is False


class TestDVal03ColDisturbance:
    """D-VAL-03 — G0 column 1 disturbed → invalid."""

    def test_d_val_03_g0_col_one_disturbed_invalid(self) -> None:
        # Arrange
        validator = MagicSquareValidator()
        disturbed = disturbed_col_one(GRID_G0)

        # Act
        result = validator.validate_complete(disturbed)

        # Assert
        assert result.valid is False


class TestDVal04DiagonalDisturbance:
    """D-VAL-04 — G0 diagonal disturbed → invalid."""

    def test_d_val_04_g0_diagonal_disturbed_invalid(self) -> None:
        # Arrange
        validator = MagicSquareValidator()
        disturbed = disturbed_diagonal(GRID_G0)

        # Act
        result = validator.validate_complete(disturbed)

        # Assert
        assert result.valid is False


class TestDVal05DuplicateOnComplete:
    """D-VAL-05 — complete grid with duplicate → invalid."""

    def test_d_val_05_complete_grid_duplicate_invalid(self) -> None:
        # Arrange
        validator = MagicSquareValidator()
        disturbed = duplicate_complete_grid(GRID_G0)

        # Act
        result = validator.validate_complete(disturbed)

        # Assert
        assert result.valid is False


class TestDVal06ZeroOnComplete:
    """D-VAL-06 — complete grid still containing 0 → invalid."""

    def test_d_val_06_complete_grid_with_zero_invalid(self) -> None:
        # Arrange
        validator = MagicSquareValidator()
        disturbed = zero_on_complete_grid(GRID_G0)

        # Act
        result = validator.validate_complete(disturbed)

        # Assert
        assert result.valid is False
