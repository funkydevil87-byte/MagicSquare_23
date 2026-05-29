"""U-IN-05 — non-zero duplicate (E005)."""

from __future__ import annotations

from unittest.mock import patch

from magicsquare.boundary.input_validator import InputValidator
from tests.boundary.conftest import (
    DUPLICATE_VALUE_CODE,
    DUPLICATE_VALUE_MESSAGE,
    EXECUTE_PATCH,
    GRID_DUPLICATE,
    FailureResult,
)


class TestUIn05Duplicate:
    """FR-01 / AC-FR01-08 — DUPLICATE_VALUE failure envelope."""

    def test_u_in_05_duplicate_nonzero_returns_e005(self) -> None:
        validator = InputValidator()
        result = validator.validate(GRID_DUPLICATE)
        assert isinstance(result, FailureResult)
        assert result.code == DUPLICATE_VALUE_CODE
        assert result.message == DUPLICATE_VALUE_MESSAGE

    @patch(EXECUTE_PATCH)
    def test_u_in_05_boundary_solve_does_not_execute(
        self, execute_mock, boundary
    ) -> None:
        boundary.solve(GRID_DUPLICATE)
        execute_mock.assert_not_called()
