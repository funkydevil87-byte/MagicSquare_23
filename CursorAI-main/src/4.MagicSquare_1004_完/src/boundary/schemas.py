"""Pydantic schemas for Boundary success and failure responses."""

from __future__ import annotations

from pydantic import BaseModel


class ErrorDetail(BaseModel):
    """Error payload nested inside a failure response envelope.

    Attributes:
        code: Machine-readable error identifier (e.g. INVALID_SIZE).
        message: Human-readable error description for the caller.
    """

    code: str
    message: str


class FailureResponse(BaseModel):
    """Standard failure envelope returned by Boundary on contract violation.

    Attributes:
        type: Response discriminator; always ``"ERROR"`` for failures.
        error: Nested code and message describing the validation failure.
    """

    type: str
    error: ErrorDetail


class SuccessResponse(BaseModel):
    """Standard success envelope returned by Boundary on solve completion.

    Attributes:
        type: Response discriminator; always ``"OK"`` for successes.
        data: Six-element result ``[r1, c1, n1, r2, c2, n2]`` (1-index).
    """

    type: str
    data: list[int]
