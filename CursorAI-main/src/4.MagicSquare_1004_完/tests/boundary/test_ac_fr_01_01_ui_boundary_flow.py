"""AC-FR-01-01 UIBoundary flow RED tests — Domain resolve() call isolation.

AC-FR-01-01, PRD §8.1 INVALID_SIZE — grid=None must not invoke resolve().
"""

from __future__ import annotations

from unittest.mock import MagicMock

import pytest

from boundary.schemas import FailureResponse
from boundary.ui_boundary import UIBoundary
from control.solve_partial_magic_square import SolvePartialMagicSquare

from tests.boundary.ac_fr_01_01_constants import INVALID_SIZE_CODE, INVALID_SIZE_MESSAGE


class TestResolveIsolation:
    """격리 검증 — grid=None 시 resolve() 0회 호출 (mock/spy)."""

    def test_none_grid_resolve_never_called_spy(self, grid_none: None) -> None:
        """AC-FR-01-01, PRD §8.1 INVALID_SIZE — resolve() spy assert_not_called."""
        # AC-FR-01-01
        # Given
        mock_resolve = MagicMock(spec=SolvePartialMagicSquare)
        boundary = UIBoundary(solve_use_case=mock_resolve)

        # When
        result = boundary.solve(grid_none)

        # Then
        mock_resolve.resolve.assert_not_called()
        assert result.type == "ERROR"
        assert result.error.code == INVALID_SIZE_CODE

    def test_none_grid_mock_resolve_call_count_zero(self, grid_none: None) -> None:
        """AC-FR-01-01, PRD §8.1 INVALID_SIZE — resolve() call_count == 0."""
        # AC-FR-01-01
        # Given
        mock_resolve = MagicMock()
        mock_resolve.resolve = MagicMock()
        boundary = UIBoundary(solve_use_case=mock_resolve)

        # When
        boundary.solve(grid_none)

        # Then
        assert mock_resolve.resolve.call_count == 0

    def test_none_grid_resolve_spy_raises_when_called(self) -> None:
        """AC-FR-01-01, PRD §8.1 INVALID_SIZE — spy must fail if resolve() invoked."""
        # AC-FR-01-01
        # Given
        mock_resolve = MagicMock()

        # When — simulate Boundary bug: resolve invoked despite None grid
        mock_resolve.resolve(None)

        # Then — RED guard: assert_not_called() must raise AssertionError
        with pytest.raises(AssertionError):
            mock_resolve.resolve.assert_not_called()

    def test_none_grid_boundary_returns_failure_without_domain_entry(
        self, grid_none: None
    ) -> None:
        """AC-FR-01-01, PRD §8.1 INVALID_SIZE — FailureResponse without resolve()."""
        # AC-FR-01-01
        # Given
        mock_resolve = MagicMock(spec=SolvePartialMagicSquare)
        boundary = UIBoundary(solve_use_case=mock_resolve)

        # When
        result = boundary.solve(grid_none)

        # Then
        mock_resolve.resolve.assert_not_called()
        assert isinstance(result, FailureResponse)
        assert result.error.message == INVALID_SIZE_MESSAGE
