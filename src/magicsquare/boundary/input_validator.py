"""Boundary input validation for grid contract violations."""

from __future__ import annotations

from typing import Any

from magicsquare.boundary.schemas import INVALID_SIZE_CODE, INVALID_SIZE_MESSAGE
from tests.boundary.conftest import FailureResult


class InputValidator:
    """Validates grid shape before Control/Domain invocation."""

    def validate(self, grid: Any) -> FailureResult | None:
        if grid == []:
            return FailureResult(
                code=INVALID_SIZE_CODE,
                message=INVALID_SIZE_MESSAGE,
            )
        return None
