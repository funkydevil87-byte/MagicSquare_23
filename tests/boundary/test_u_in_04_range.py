"""U-IN-04 — value range violations (E004)."""

from __future__ import annotations

from unittest.mock import patch

from magicsquare.boundary.input_validator import InputValidator
from tests.boundary.conftest import (
    EXECUTE_PATCH,
    GRID_MINUS_ONE,
    GRID_SEVENTEEN,
    OUT_OF_RANGE_CODE,
    OUT_OF_RANGE_MESSAGE,
    FailureResult,
)


class TestUIn04Range:
    """FR-01 / AC-FR01-07 — OUT_OF_RANGE failure envelope."""

    def test_u_in_04a_minus_one_returns_e004(self) -> None:
        validator = InputValidator()
        result = validator.validate(GRID_MINUS_ONE)
        assert isinstance(result, FailureResult)
        assert result.code == OUT_OF_RANGE_CODE
        assert result.message == OUT_OF_RANGE_MESSAGE

    def test_u_in_04b_seventeen_returns_e004(self) -> None:
        validator = InputValidator()
        result = validator.validate(GRID_SEVENTEEN)
        assert isinstance(result, FailureResult)
        assert result.code == OUT_OF_RANGE_CODE
        assert result.message == OUT_OF_RANGE_MESSAGE

    @patch(EXECUTE_PATCH)
    def test_u_in_04a_boundary_solve_does_not_execute(
        self, execute_mock, boundary
    ) -> None:
        boundary.solve(GRID_MINUS_ONE)
        execute_mock.assert_not_called()
