"""Validation outcome for complete magic square grids."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class ValidationResult:
    """Result of validating a complete 4x4 grid."""

    valid: bool
