"""D-T22 / TD-07 — both-valid attempts prefer Attempt 1 (UC-D6)."""

from __future__ import annotations

from unittest.mock import patch

from magicsquare.control.solve_partial_magic_square import SolvePartialMagicSquare
from tests.conftest import GRID_G1


class TestDSol22BothValid:
    """When both attempts validate, small-first (Attempt 1) wins."""

    @patch(
        "magicsquare.entity.services.magic_square_validator.MagicSquareValidator.validate_complete"
    )
    def test_d_sol_22_both_valid_prefers_attempt_one(self, validate_mock) -> None:
        validate_mock.return_value = type("VR", (), {"valid": True})()
        solver = SolvePartialMagicSquare()
        result = solver.execute(GRID_G1)
        assert result == [2, 2, 7, 3, 3, 10]
