"""AC-FR-01-01 Boundary input validation RED tests.

AC-FR-01-01, PRD §8.1 INVALID_SIZE — null/size invalid grid failure contract.
"""

from __future__ import annotations

import pytest
from pydantic import BaseModel

from boundary.input_validator import InputValidator
from boundary.schemas import ErrorDetail, FailureResponse

from tests.boundary.ac_fr_01_01_constants import (
    AC_FR_01_01,
    EXCLUDED_AC_IDS,
    EXCLUDED_FR_IDS,
    FORBIDDEN_SCENARIO_TAGS,
    IN_SCOPE_SCENARIO_TAGS,
    INVALID_SIZE_CODE,
    INVALID_SIZE_MESSAGE,
)


class TestNormalFailureReturn:
    """정상 실패 반환 — grid=None → INVALID_SIZE failure envelope."""

    def test_none_grid_returns_failure_with_invalid_size_code(
        self, grid_none: None
    ) -> None:
        """AC-FR-01-01, PRD §8.1 INVALID_SIZE — None grid yields failure response."""
        # AC-FR-01-01
        # Given
        validator = InputValidator()

        # When
        result = validator.validate(grid_none)

        # Then
        assert result.type == "ERROR"
        assert result.error.code == INVALID_SIZE_CODE
        assert result.error.message == INVALID_SIZE_MESSAGE


class TestBoundaryValues:
    """경계값 — empty list, four empty rows, 3×4 size mismatch."""

    @pytest.mark.parametrize(
        "grid_fixture",
        ["grid_empty_list", "grid_four_empty_rows", "grid_3x4"],
        ids=["empty_list", "four_empty_rows", "size_3x4"],
    )
    def test_invalid_size_grid_returns_failure_result(
        self, grid_fixture: str, request: pytest.FixtureRequest
    ) -> None:
        """AC-FR-01-01, PRD §8.1 INVALID_SIZE — size-violating grids fail at Boundary."""
        # AC-FR-01-01
        # Given
        grid = request.getfixturevalue(grid_fixture)
        validator = InputValidator()

        # When
        result = validator.validate(grid)

        # Then
        assert result.type == "ERROR"
        assert result.error.code == INVALID_SIZE_CODE
        assert result.error.message == INVALID_SIZE_MESSAGE


class TestMessageExactMatch:
    """메시지 동일성 — PRD §8.1 문구와 문자 단위 비교."""

    def test_none_grid_message_matches_prd_section_8_1_exactly(
        self, grid_none: None
    ) -> None:
        """AC-FR-01-01, PRD §8.1 INVALID_SIZE — message char-by-char identity."""
        # AC-FR-01-01
        # Given
        expected_message = "Grid must be 4x4."
        validator = InputValidator()

        # When
        result = validator.validate(grid_none)

        # Then
        assert result.error.message == expected_message
        assert len(result.error.message) == len(expected_message)
        assert list(result.error.message) == list(expected_message)

    def test_none_grid_returns_exact_invalid_size_code_string(
        self, grid_none: None
    ) -> None:
        """AC-FR-01-01, PRD §8.1 INVALID_SIZE — code string exact match."""
        # AC-FR-01-01
        # Given
        validator = InputValidator()

        # When
        result = validator.validate(grid_none)

        # Then
        assert result.error.code == "INVALID_SIZE"
        assert result.error.code is not None
        assert isinstance(result.error.code, str)


class TestFailureResponseStructure:
    """반환 객체 타입 — pydantic FailureResponse 구조체 검증."""

    def test_none_grid_returns_pydantic_failure_response_type(
        self, grid_none: None
    ) -> None:
        """AC-FR-01-01, PRD §8.1 INVALID_SIZE — FailureResponse pydantic model."""
        # AC-FR-01-01
        # Given
        validator = InputValidator()

        # When
        result = validator.validate(grid_none)

        # Then
        assert isinstance(result, FailureResponse)
        assert isinstance(result.error, ErrorDetail)
        assert issubclass(FailureResponse, BaseModel)
        assert result.model_dump() == {
            "type": "ERROR",
            "error": {
                "code": INVALID_SIZE_CODE,
                "message": INVALID_SIZE_MESSAGE,
            },
        }


class TestScopeRestriction:
    """범위 제한 — AC-FR-01-02~05, FR-02~05 케이스 포함 금지."""

    def test_ac_fr_01_01_scope_excludes_later_acceptance_criteria(self) -> None:
        """AC-FR-01-01, PRD §8.1 INVALID_SIZE — scope registry excludes later AC/FR."""
        # AC-FR-01-01
        # Given
        in_scope_ac = {AC_FR_01_01}

        # When / Then
        assert in_scope_ac.isdisjoint(EXCLUDED_AC_IDS)
        assert AC_FR_01_01 in in_scope_ac
        assert IN_SCOPE_SCENARIO_TAGS.isdisjoint(FORBIDDEN_SCENARIO_TAGS)
        assert "FR-01" not in EXCLUDED_FR_IDS

    def test_ac_fr_01_01_scope_module_covers_only_null_and_size_tags(self) -> None:
        """AC-FR-01-01, PRD §8.1 INVALID_SIZE — no FR-02~05 scenario tags in scope."""
        # AC-FR-01-01
        # Given
        active_scope = IN_SCOPE_SCENARIO_TAGS

        # When / Then
        assert active_scope <= {"null", "empty_list", "four_empty_rows", "size_3x4"}
        for fr_id in EXCLUDED_FR_IDS:
            assert fr_id.startswith("FR-")
        for ac_id in EXCLUDED_AC_IDS:
            assert ac_id.startswith("AC-FR-01-")
