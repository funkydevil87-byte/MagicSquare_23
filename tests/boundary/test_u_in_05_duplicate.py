"""U-IN-05 — non-zero duplicate (E005). Track A Boundary RED skeleton."""

from __future__ import annotations

import pytest


class TestUIn05Duplicate:
    """FR-01 / AC-FR01-08 — DUPLICATE_VALUE → E005 failure envelope."""

    def test_u_in_05_duplicate_nonzero_returns_e005(self) -> None:
        # U-IN-05
        # from magicsquare.boundary.input_validator import InputValidator
        # Given: 4×4 grid, two blanks, duplicate non-zero value (0 excluded)
        # validator = InputValidator()
        # grid = ...  # e.g. TD-05 style duplicate
        # When: validator.validate(grid)
        pytest.fail(
            "RED: U-IN-05 — duplicate non-zero yields E005 envelope, Domain execute 0×"
        )
