"""Control-layer exceptions."""

from __future__ import annotations


class SolveUnsolvableError(Exception):
    """Raised when Control orchestration cannot produce a valid solution."""
