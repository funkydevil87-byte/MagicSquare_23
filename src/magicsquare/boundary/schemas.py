"""Boundary failure and validation contract models."""

from __future__ import annotations

from pydantic import BaseModel

INVALID_SIZE_CODE = "INVALID_SIZE"
INVALID_SIZE_MESSAGE = "Grid must be 4x4."
GRID_SIZE = 4


class FailureResult(BaseModel):
    """Failure payload returned by Boundary when input validation fails."""

    code: str
    message: str
