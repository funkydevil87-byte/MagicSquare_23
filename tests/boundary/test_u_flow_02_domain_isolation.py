"""U-FLOW-02 — invalid input must not invoke Control.execute."""

from __future__ import annotations

from typing import Any
from unittest.mock import patch

import pytest

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
    FailureResult,
)


def _assert_failure(result: Any, code: str) -> FailureResult:
    assert isinstance(result, FailureResult)
    assert result.code == code
    return result


class TestUFlow02DomainIsolation:
    """FR-01 + AC-FR01-01 — short-circuit invalid → execute.call_count == 0."""

    @patch(EXECUTE_PATCH)
    def test_u_flow_02a_null_matrix_execute_zero_e003(
        self, execute_mock: Any, boundary: Any
    ) -> None:
        result = boundary.solve(None)
        _assert_failure(result, NULL_INPUT_CODE)
        execute_mock.assert_not_called()

    @patch(EXECUTE_PATCH)
    def test_u_flow_02b_invalid_size_execute_zero_e001(
        self, execute_mock: Any, boundary: Any
    ) -> None:
        result = boundary.solve(GRID_3X4)
        _assert_failure(result, INVALID_ROW_COUNT_CODE)
        execute_mock.assert_not_called()

    @patch(EXECUTE_PATCH)
    def test_u_flow_02c_invalid_blank_count_execute_zero_e002(
        self, execute_mock: Any, boundary: Any
    ) -> None:
        for grid in (GRID_NO_BLANKS, GRID_THREE_BLANKS):
            result = boundary.solve(grid)
            _assert_failure(result, INVALID_EMPTY_COUNT_CODE)
            execute_mock.assert_not_called()

    @patch(EXECUTE_PATCH)
    def test_u_flow_02d_out_of_range_execute_zero_e004(
        self, execute_mock: Any, boundary: Any
    ) -> None:
        result = boundary.solve(GRID_MINUS_ONE)
        _assert_failure(result, OUT_OF_RANGE_CODE)
        execute_mock.assert_not_called()

    @patch(EXECUTE_PATCH)
    def test_u_flow_02e_duplicate_execute_zero_e005(
        self, execute_mock: Any, boundary: Any
    ) -> None:
        result = boundary.solve(GRID_DUPLICATE)
        _assert_failure(result, DUPLICATE_VALUE_CODE)
        execute_mock.assert_not_called()

    @patch(EXECUTE_PATCH)
    def test_u_flow_02b_jagged_cols_execute_zero(
        self, execute_mock: Any, boundary: Any
    ) -> None:
        result = boundary.solve(GRID_EMPTY_COLS)
        _assert_failure(result, INVALID_COL_COUNT_CODE)
        execute_mock.assert_not_called()
