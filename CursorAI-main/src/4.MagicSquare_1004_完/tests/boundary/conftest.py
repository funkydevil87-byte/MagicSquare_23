"""Shared fixtures for AC-FR-01-01 Boundary RED tests."""

from __future__ import annotations

import pytest

from tests.boundary.ac_fr_01_01_constants import (
    INVALID_SIZE_CODE,
    INVALID_SIZE_MESSAGE,
)


@pytest.fixture
def invalid_size_code() -> str:
    """Expected error code for null/size violations under AC-FR-01-01."""
    return INVALID_SIZE_CODE


@pytest.fixture
def invalid_size_message() -> str:
    """Expected error message for null/size violations under AC-FR-01-01."""
    return INVALID_SIZE_MESSAGE


@pytest.fixture
def grid_none() -> None:
    """Explicit None grid input (BV-01)."""
    return None


@pytest.fixture
def grid_empty_list() -> list[list[int]]:
    """Empty outer list — zero rows (BV-02)."""
    return []


@pytest.fixture
def grid_four_empty_rows() -> list[list[int]]:
    """Four rows with zero columns each (BV-03)."""
    return [[]] * 4


@pytest.fixture
def grid_3x4() -> list[list[int]]:
    """Three rows, four columns — row count mismatch (BV-04)."""
    return [[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12]]
