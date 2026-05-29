"""Adapters and I/O boundary layer."""

from magicsquare.boundary.input_validator import InputValidator
from magicsquare.boundary.magic_square_boundary import MagicSquareBoundary
from magicsquare.boundary.schemas import (
    INVALID_SIZE_CODE,
    INVALID_SIZE_MESSAGE,
    FailureResult,
)

__all__ = [
    "FailureResult",
    "InputValidator",
    "INVALID_SIZE_CODE",
    "INVALID_SIZE_MESSAGE",
    "MagicSquareBoundary",
]

