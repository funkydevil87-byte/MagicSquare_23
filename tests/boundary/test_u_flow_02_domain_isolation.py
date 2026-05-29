"""U-FLOW-02 — invalid input must not invoke Control.execute."""

from __future__ import annotations

from typing import Any
from unittest.mock import patch

import pytest

from magicsquare.boundary.exceptions import BoundaryValidationError
from tests.boundary.conftest import (
    DUPLICATE_VALUE_CODE,
    EXECUTE_PATCH,
    GRID_3X4,
    GRID_DUPLICATE,
    GRID_EMPTY_COLS,
    GRID_MINUS_ONE,
    GRID_NO_BLANKS,
    GRID_THREE_BLANKS,
    INVALID_COL_COUNT_CODE,
    INVALID_EMPTY_COUNT_CODE,
    INVALID_ROW_COUNT_CODE,
    NULL_INPUT_CODE,
    OUT_OF_RANGE_CODE,
)


def _assert_validation_failure(boundary: Any, grid: Any, code: str) -> None:
    with pytest.raises(BoundaryValidationError) as exc_info:
        boundary.solve(grid)
    assert exc_info.value.code == code


class TestUFlow02DomainIsolation:
    """FR-01 + AC-FR01-01 — short-circuit invalid → execute.call_count == 0."""

    @patch(EXECUTE_PATCH)
    def test_u_flow_02a_null_matrix_execute_zero_e003(
        self, execute_mock: Any, boundary: Any
    ) -> None:
        _assert_validation_failure(boundary, None, NULL_INPUT_CODE)
        execute_mock.assert_not_called()

    @patch(EXECUTE_PATCH)
    def test_u_flow_02b_invalid_size_execute_zero_e001(
        self, execute_mock: Any, boundary: Any
    ) -> None:
        _assert_validation_failure(boundary, GRID_3X4, INVALID_ROW_COUNT_CODE)
        execute_mock.assert_not_called()

    @patch(EXECUTE_PATCH)
    def test_u_flow_02c_invalid_blank_count_execute_zero_e002(
        self, execute_mock: Any, boundary: Any
    ) -> None:
        for grid in (GRID_NO_BLANKS, GRID_THREE_BLANKS):
            _assert_validation_failure(boundary, grid, INVALID_EMPTY_COUNT_CODE)
            execute_mock.assert_not_called()

    @patch(EXECUTE_PATCH)
    def test_u_flow_02d_out_of_range_execute_zero_e004(
        self, execute_mock: Any, boundary: Any
    ) -> None:
        _assert_validation_failure(boundary, GRID_MINUS_ONE, OUT_OF_RANGE_CODE)
        execute_mock.assert_not_called()

    @patch(EXECUTE_PATCH)
    def test_u_flow_02e_duplicate_execute_zero_e005(
        self, execute_mock: Any, boundary: Any
    ) -> None:
        _assert_validation_failure(boundary, GRID_DUPLICATE, DUPLICATE_VALUE_CODE)
        execute_mock.assert_not_called()

    @patch(EXECUTE_PATCH)
    def test_u_flow_02b_jagged_cols_execute_zero(
        self, execute_mock: Any, boundary: Any
    ) -> None:
        _assert_validation_failure(boundary, GRID_EMPTY_COLS, INVALID_COL_COUNT_CODE)
        execute_mock.assert_not_called()
