"""Domain-layer exceptions (no Boundary error codes)."""

from __future__ import annotations


class UnsolvableDomainError(Exception):
    """Raised when neither attempt produces a valid magic square."""
