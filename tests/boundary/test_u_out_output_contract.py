"""U-OUT-01~03 — success output contract. Track A Boundary RED skeleton."""

from __future__ import annotations

import pytest

# U-OUT only: Control test double allowed (Domain logic mock forbidden)
# from magicsquare.boundary.ui_boundary import UIBoundary
# @patch("magicsquare.control.solve_partial_magic_square.SolvePartialMagicSquare.execute")


class TestUOutOutputContract:
    """FR-05-B — success int[6] shape with G1 and execute stub."""

    def test_u_out_01_g1_success_vector_length_six(self) -> None:
        # U-OUT-01
        # Given: G1 valid partial grid; execute stub returns fixed int[6]
        # boundary = UIBoundary()
        # When: boundary.solve(GRID_G1) with patched execute
        pytest.fail("RED: U-OUT-01 — G1 + execute stub returns success data length 6")

    def test_u_out_02_g1_coordinates_one_indexed(self) -> None:
        # U-OUT-02
        # Given: G1 + execute stub returning [2,2,7,3,3,10]
        # boundary = UIBoundary()
        # When: boundary.solve(GRID_G1)
        pytest.fail("RED: U-OUT-02 — r1,c1,r2,c2 in [1,4] (1-index, BR-14)")

    def test_u_out_03_g1_missing_values_in_range(self) -> None:
        # U-OUT-03
        # Given: G1 + execute stub; n1,n2 are the two missing numbers
        # boundary = UIBoundary()
        # When: boundary.solve(GRID_G1)
        pytest.fail("RED: U-OUT-03 — n1,n2 ∈ [1,16] and n1≠n2 on success path")
