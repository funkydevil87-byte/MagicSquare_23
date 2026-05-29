"""Boundary failure and validation contract models."""

from __future__ import annotations

from pydantic import BaseModel

GRID_SIZE = 4

# AC-FR-01-01 legacy slice (size/null family — kept for traceability)
INVALID_SIZE_CODE = "INVALID_SIZE"
INVALID_SIZE_MESSAGE = "Grid must be 4x4."

# FR-01 / Report/09 E-envelope + PRD §13.1 codes
NULL_INPUT_CODE = "NULL_INPUT"
NULL_INPUT_MESSAGE = "Input matrix must not be null."

INVALID_ROW_COUNT_CODE = "INVALID_ROW_COUNT"
INVALID_ROW_COUNT_MESSAGE = "행 개수는 4여야 합니다"

INVALID_COL_COUNT_CODE = "INVALID_COL_COUNT"
INVALID_COL_COUNT_MESSAGE = "열 개수는 4여야 합니다"

INVALID_EMPTY_COUNT_CODE = "INVALID_EMPTY_COUNT"
INVALID_EMPTY_COUNT_MESSAGE = "Exactly two blank cells (0) required."

OUT_OF_RANGE_CODE = "OUT_OF_RANGE"
OUT_OF_RANGE_MESSAGE = "Each value must be 0 or in 1..16."

DUPLICATE_VALUE_CODE = "DUPLICATE_VALUE"
DUPLICATE_VALUE_MESSAGE = "Non-zero values must be unique."


class FailureResult(BaseModel):
    """Failure payload returned by Boundary when input validation fails."""

    code: str
    message: str
