"""Boundary-layer exceptions for public API failure signaling."""

from __future__ import annotations

UNSOLVABLE_CODE = "UNSOLVABLE"
UNSOLVABLE_MESSAGE = "주어진 배치로는 마방진을 완성할 수 없습니다"


class BoundaryValidationError(Exception):
    """Raised when input validation fails (E001~E005)."""

    def __init__(self, code: str, message: str) -> None:
        super().__init__(message)
        self.code = code
        self.message = message


class UnsolvableError(Exception):
    """Raised when both solve attempts fail (E006)."""

    def __init__(self) -> None:
        super().__init__(UNSOLVABLE_MESSAGE)
        self.code = UNSOLVABLE_CODE
        self.message = UNSOLVABLE_MESSAGE
