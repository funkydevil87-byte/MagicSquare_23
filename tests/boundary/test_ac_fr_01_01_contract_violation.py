"""AC-FR-01-01, PRD §8.1 INVALID_SIZE — contract violation must not invoke Domain resolve()."""

from __future__ import annotations

import ast
from pathlib import Path
from typing import Any
from unittest.mock import patch

import pytest

from tests.boundary.conftest import (
    GRID_3X4,
    GRID_EMPTY_COLS,
    PRD_INVALID_SIZE_CODE,
    PRD_INVALID_SIZE_MESSAGE,
    RESOLVE_PATCH,
    FailureResult,
)

MODULE_PATH = Path(__file__)
FORBIDDEN_ERROR_CODES = frozenset(
    {
        "NULL_INPUT",
        "INVALID_ROW_COUNT",
        "INVALID_COL_COUNT",
        "INVALID_EMPTY_COUNT",
        "OUT_OF_RANGE",
        "DUPLICATE_VALUE",
        "UNSOLVABLE",
    }
)
FORBIDDEN_DOMAIN_IMPORTS = frozenset(
    {
        "BlankFinder",
        "MissingNumberFinder",
        "MagicSquareValidator",
        "PartialMagicSquareSolver",
    }
)


def _module_ast() -> ast.Module:
    return ast.parse(MODULE_PATH.read_text(encoding="utf-8"))


def _grid_literal_values(tree: ast.AST) -> list[Any]:
    values: list[Any] = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name) and target.id.startswith("GRID_"):
                    values.append(_eval_static_literal(node.value))
    return values


def _eval_static_literal(node: ast.AST) -> Any:
    if isinstance(node, ast.Constant):
        return node.value
    if isinstance(node, ast.List):
        return [_eval_static_literal(elt) for elt in node.elts]
    if isinstance(node, ast.BinOp) and isinstance(node.op, ast.Mult):
        left = _eval_static_literal(node.left)
        right = _eval_static_literal(node.right)
        if isinstance(left, list) and isinstance(right, int):
            return left * right
    if isinstance(node, ast.Name):
        return node.id
    return None


def _asserted_failure_codes(tree: ast.AST) -> set[str]:
    codes: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Compare):
            for comparator in node.comparators:
                if isinstance(comparator, ast.Constant) and isinstance(
                    comparator.value, str
                ):
                    codes.add(comparator.value)
    return codes


def _assert_failure_result(result: Any) -> FailureResult:
    assert isinstance(result, FailureResult)
    return result


class TestNormalFailureReturn:
    """AC-FR-01-01, PRD §8.1 INVALID_SIZE — happy path of failure for invalid grid input."""

    def test_none_grid_returns_failure_result_not_success(
        self, boundary: Any
    ) -> None:
        # AC-FR-01-01
        # Given: grid is explicitly None
        grid = None

        # When: Boundary processes the invalid grid
        result = boundary.solve(grid)

        # Then: a failure result is returned instead of a success vector
        failure = _assert_failure_result(result)
        assert failure.code == PRD_INVALID_SIZE_CODE

    def test_none_grid_failure_code_is_invalid_size(self, boundary: Any) -> None:
        # AC-FR-01-01
        # Given: grid is None
        grid = None

        # When: Boundary returns the contract failure
        result = boundary.solve(grid)

        # Then: code is exactly INVALID_SIZE
        failure = _assert_failure_result(result)
        assert failure.code == "INVALID_SIZE"

    def test_none_grid_failure_message_is_present(self, boundary: Any) -> None:
        # AC-FR-01-01
        # Given: grid is None
        grid = None

        # When: Boundary returns the contract failure
        result = boundary.solve(grid)

        # Then: message field is populated with the PRD text
        failure = _assert_failure_result(result)
        assert failure.message == PRD_INVALID_SIZE_MESSAGE

    def test_none_grid_failure_is_pydantic_model(self, boundary: Any) -> None:
        # AC-FR-01-01
        # Given: grid is None
        grid = None

        # When: Boundary materializes the failure payload
        result = boundary.solve(grid)

        # Then: the payload conforms to FailureResult
        failure = _assert_failure_result(result)
        assert failure.model_dump() == {
            "code": PRD_INVALID_SIZE_CODE,
            "message": PRD_INVALID_SIZE_MESSAGE,
        }

    def test_none_grid_does_not_return_success_int_vector(self, boundary: Any) -> None:
        # AC-FR-01-01
        # Given: grid is None
        grid = None

        # When: Boundary handles the request
        result = boundary.solve(grid)

        # Then: success shape int[6] is never returned
        assert not isinstance(result, list)
        _assert_failure_result(result)


class TestBoundaryValues:
    """AC-FR-01-01, PRD §8.1 INVALID_SIZE — size-mismatch boundary inputs fail at Boundary."""

    def test_empty_list_grid_returns_failure_result(self, boundary: Any) -> None:
        # AC-FR-01-01
        # Given: grid is an empty list (zero rows)
        grid: list[list[int]] = []

        # When: Boundary validates the grid
        result = boundary.solve(grid)

        # Then: failure result is returned
        _assert_failure_result(result)

    def test_empty_cols_grid_returns_failure_result(self, boundary: Any) -> None:
        # AC-FR-01-01
        # Given: grid has four rows but zero columns
        grid = GRID_EMPTY_COLS

        # When: Boundary validates the grid
        result = boundary.solve(grid)

        # Then: failure result is returned
        _assert_failure_result(result)

    def test_3x4_grid_returns_failure_result(self, boundary: Any) -> None:
        # AC-FR-01-01
        # Given: grid is 3 rows by 4 columns
        grid = GRID_3X4

        # When: Boundary validates the grid
        result = boundary.solve(grid)

        # Then: failure result is returned
        _assert_failure_result(result)

    def test_empty_list_failure_code_is_invalid_size(self, boundary: Any) -> None:
        # AC-FR-01-01
        # Given: grid is []
        grid: list[list[int]] = []

        # When: Boundary returns failure
        result = boundary.solve(grid)

        # Then: code is INVALID_SIZE
        failure = _assert_failure_result(result)
        assert failure.code == PRD_INVALID_SIZE_CODE

    def test_3x4_failure_message_matches_invalid_size_text(self, boundary: Any) -> None:
        # AC-FR-01-01
        # Given: grid is 3×4
        grid = GRID_3X4

        # When: Boundary returns failure
        result = boundary.solve(grid)

        # Then: message matches PRD §8.1 INVALID_SIZE wording
        failure = _assert_failure_result(result)
        assert failure.message == PRD_INVALID_SIZE_MESSAGE


class TestIsolationVerification:
    """AC-FR-01-01, PRD §8.1 INVALID_SIZE — Domain resolve() must remain uninvoked."""

    @patch(RESOLVE_PATCH)
    def test_none_grid_resolve_zero_calls_spy(
        self, mock_resolve: Any, boundary: Any
    ) -> None:
        # AC-FR-01-01
        # Given: grid is None and resolve() is spied
        grid = None

        # When: Boundary handles the invalid request
        boundary.solve(grid)

        # Then: Domain resolve() is never entered
        mock_resolve.assert_not_called()

    @patch(RESOLVE_PATCH)
    def test_empty_list_resolve_zero_calls_spy(
        self, mock_resolve: Any, boundary: Any
    ) -> None:
        # AC-FR-01-01
        # Given: grid is [] and resolve() is spied
        grid: list[list[int]] = []

        # When: Boundary handles the invalid request
        boundary.solve(grid)

        # Then: Domain resolve() is never entered
        mock_resolve.assert_not_called()

    @patch(RESOLVE_PATCH)
    def test_empty_cols_resolve_zero_calls_spy(
        self, mock_resolve: Any, boundary: Any
    ) -> None:
        # AC-FR-01-01
        # Given: grid is [[]]*4 and resolve() is spied
        grid = GRID_EMPTY_COLS

        # When: Boundary handles the invalid request
        boundary.solve(grid)

        # Then: Domain resolve() is never entered
        mock_resolve.assert_not_called()

    @patch(RESOLVE_PATCH)
    def test_3x4_grid_resolve_zero_calls_spy(
        self, mock_resolve: Any, boundary: Any
    ) -> None:
        # AC-FR-01-01
        # Given: grid is 3×4 and resolve() is spied
        grid = GRID_3X4

        # When: Boundary handles the invalid request
        boundary.solve(grid)

        # Then: Domain resolve() is never entered
        mock_resolve.assert_not_called()

    @patch(RESOLVE_PATCH)
    def test_none_grid_resolve_call_count_is_exactly_zero(
        self, mock_resolve: Any, boundary: Any
    ) -> None:
        # AC-FR-01-01
        # Given: grid is None with an active resolve() spy
        grid = None

        # When: Boundary completes failure handling
        boundary.solve(grid)

        # Then: call_count remains zero (mock failure if invoked)
        assert mock_resolve.call_count == 0
        mock_resolve.assert_not_called()


class TestMessageIdentity:
    """AC-FR-01-01, PRD §8.1 INVALID_SIZE — message must match PRD text character-for-character."""

    @pytest.mark.parametrize(
        "grid",
        [
            None,
            [],
            GRID_EMPTY_COLS,
            GRID_3X4,
        ],
        ids=["none", "empty_list", "empty_cols", "grid_3x4"],
    )
    def test_invalid_grid_message_exact_prd_section_8_1(
        self, boundary: Any, grid: list[list[int]] | None
    ) -> None:
        # AC-FR-01-01
        # Given: an in-scope invalid grid fixture
        # When: Boundary returns INVALID_SIZE failure
        result = boundary.solve(grid)

        # Then: message equals PRD §8.1 text with character-level equality
        failure = _assert_failure_result(result)
        assert failure.message == PRD_INVALID_SIZE_MESSAGE
        assert list(failure.message) == list(PRD_INVALID_SIZE_MESSAGE)

    def test_none_grid_message_length_matches_prd_text(self, boundary: Any) -> None:
        # AC-FR-01-01
        # Given: grid is None
        grid = None

        # When: Boundary returns failure message
        result = boundary.solve(grid)

        # Then: message length matches PRD §8.1 exactly
        failure = _assert_failure_result(result)
        assert len(failure.message) == len(PRD_INVALID_SIZE_MESSAGE)

    def test_none_grid_code_exact_invalid_size_string(self, boundary: Any) -> None:
        # AC-FR-01-01
        # Given: grid is None
        grid = None

        # When: Boundary returns failure code
        result = boundary.solve(grid)

        # Then: code string equals INVALID_SIZE with no surrounding whitespace
        failure = _assert_failure_result(result)
        assert failure.code == PRD_INVALID_SIZE_CODE
        assert failure.code.strip() == failure.code

    def test_empty_list_message_no_extra_whitespace(self, boundary: Any) -> None:
        # AC-FR-01-01
        # Given: grid is []
        grid: list[list[int]] = []

        # When: Boundary returns failure message
        result = boundary.solve(grid)

        # Then: message has no leading or trailing whitespace beyond PRD text
        failure = _assert_failure_result(result)
        assert failure.message == PRD_INVALID_SIZE_MESSAGE
        assert failure.message.strip() == failure.message

    def test_3x4_message_bytes_equal_prd_literal(self, boundary: Any) -> None:
        # AC-FR-01-01
        # Given: grid is 3×4
        grid = GRID_3X4

        # When: Boundary returns failure message
        result = boundary.solve(grid)

        # Then: UTF-8 byte sequence matches PRD §8.1 literal
        failure = _assert_failure_result(result)
        assert failure.message.encode("utf-8") == PRD_INVALID_SIZE_MESSAGE.encode(
            "utf-8"
        )


class TestScopeLimitation:
    """AC-FR-01-01, PRD §8.1 INVALID_SIZE — AC-FR-01-02~05 and FR-02~05 cases stay out of scope."""

    def test_module_source_excludes_null_input_error_code(self) -> None:
        # AC-FR-01-01
        # Given: parsed AST of this RED module
        tree = _module_ast()

        # When: collecting asserted failure codes from comparisons
        asserted_codes = _asserted_failure_codes(tree)

        # Then: AC-FR-01-03 NULL_INPUT is not an expected outcome here
        assert "NULL_INPUT" not in asserted_codes

    def test_module_source_excludes_invalid_empty_count_cases(self) -> None:
        # AC-FR-01-01
        # Given: parsed AST of this RED module
        tree = _module_ast()

        # When: scanning asserted failure codes
        asserted_codes = _asserted_failure_codes(tree)

        # Then: AC-FR-01-06 INVALID_EMPTY_COUNT scenarios are not included
        assert "INVALID_EMPTY_COUNT" not in asserted_codes

    def test_module_source_excludes_out_of_range_value_cases(self) -> None:
        # AC-FR-01-01
        # Given: parsed AST grid literals
        tree = _module_ast()
        numeric_values = [
            value
            for grid in _grid_literal_values(tree)
            if isinstance(grid, list)
            for row in grid
            if isinstance(row, list)
            for value in row
            if isinstance(value, int)
        ]

        # When: scanning for AC-FR-01-07 range-violating cell values
        # Then: -1 and 17 never appear as fixture literals
        assert -1 not in numeric_values
        assert 17 not in numeric_values
        assert "OUT_OF_RANGE" not in _asserted_failure_codes(tree)

    def test_module_source_excludes_duplicate_value_cases(self) -> None:
        # AC-FR-01-01
        # Given: parsed AST of this RED module
        tree = _module_ast()

        # When: scanning asserted failure codes
        asserted_codes = _asserted_failure_codes(tree)

        # Then: AC-FR-01-08 DUPLICATE_VALUE scenarios are absent
        assert "DUPLICATE_VALUE" not in asserted_codes

    def test_module_ast_excludes_fr_02_to_fr_05_domain_imports(self) -> None:
        # AC-FR-01-01
        # Given: parsed AST of this test module
        tree = ast.parse(MODULE_PATH.read_text(encoding="utf-8"))
        imported_names = {
            alias.name
            for node in ast.walk(tree)
            if isinstance(node, ast.ImportFrom)
            for alias in node.names
        }

        # When: checking Domain component imports for FR-02~05
        # Then: BlankFinder and related FR-02~05 components are not imported
        assert imported_names.isdisjoint(FORBIDDEN_DOMAIN_IMPORTS)

    def test_in_scope_failure_codes_only_invalid_size(self, boundary: Any) -> None:
        # AC-FR-01-01
        # Given: all in-scope invalid grids for this RED commit
        grids: list[list[list[int]] | None] = [None, [], GRID_EMPTY_COLS, GRID_3X4]

        # When: each grid is processed
        for grid in grids:
            result = boundary.solve(grid)

            # Then: only INVALID_SIZE appears; forbidden codes never appear
            failure = _assert_failure_result(result)
            assert failure.code == PRD_INVALID_SIZE_CODE
            assert failure.code not in FORBIDDEN_ERROR_CODES
