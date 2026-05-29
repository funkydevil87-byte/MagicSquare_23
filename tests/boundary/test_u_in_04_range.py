"""U-IN-04 — value range violations (E004). Track A Boundary RED skeleton."""

from __future__ import annotations

import pytest


class TestUIn04Range:
    """FR-01 / AC-FR01-07 — OUT_OF_RANGE → E004 failure envelope."""

    def test_u_in_04a_minus_one_returns_e004(self) -> None:
        # U-IN-04a
        # from magicsquare.boundary.input_validator import InputValidator
        # Given: valid 4×4 shape with exactly two blanks and cell value -1
        # validator = InputValidator()
        # grid = ...  # 4×4, one cell -1
        # When: validator.validate(grid) or UIBoundary.solve(grid)
        pytest.fail("RED: U-IN-04a — cell -1 yields E004 envelope, Domain execute 0×")

    def test_u_in_04b_seventeen_returns_e004(self) -> None:
        # U-IN-04b
        # from magicsquare.boundary.input_validator import InputValidator
        # Given: valid 4×4 shape with exactly two blanks and cell value 17
        # validator = InputValidator()
        # grid = ...  # 4×4, one cell 17
        # When: validator.validate(grid)
        pytest.fail("RED: U-IN-04b — cell 17 yields E004 envelope, Domain execute 0×")
