"""U-FLOW-02 — invalid input must not invoke Control.execute. Track A RED skeleton."""

from __future__ import annotations

import pytest

# Control mock/spy (U-FLOW only):
# from magicsquare.boundary.ui_boundary import UIBoundary
# EXECUTE_PATCH = (
#     "magicsquare.control.solve_partial_magic_square.SolvePartialMagicSquare.execute"
# )
# @patch(EXECUTE_PATCH)


class TestUFlow02DomainIsolation:
    """FR-01 + AC-FR01-01 — short-circuit invalid → execute.call_count == 0 + E envelope."""

    def test_u_flow_02a_null_matrix_execute_zero_e003(self) -> None:
        # U-FLOW-02a
        # Given: matrix is None; execute spied
        # boundary = UIBoundary()
        # When: boundary.solve(None)
        pytest.fail("RED: U-FLOW-02a — null → E003 envelope, execute 0×")

    def test_u_flow_02b_invalid_size_execute_zero_e001(self) -> None:
        # U-FLOW-02b
        # Given: size ≠ 4×4 (e.g. 3×4); execute spied
        # boundary = UIBoundary()
        # When: boundary.solve(grid_3x4)
        pytest.fail("RED: U-FLOW-02b — invalid size → E001 envelope, execute 0×")

    def test_u_flow_02c_invalid_blank_count_execute_zero_e002(self) -> None:
        # U-FLOW-02c
        # Given: blank count ≠ 2 (0 or 3 zeros); execute spied
        # boundary = UIBoundary()
        # When: boundary.solve(grid_bad_blank_count)
        pytest.fail("RED: U-FLOW-02c — blank count ≠ 2 → E002 envelope, execute 0×")

    def test_u_flow_02d_out_of_range_execute_zero_e004(self) -> None:
        # U-FLOW-02d
        # Given: grid contains -1 or 17; execute spied
        # boundary = UIBoundary()
        # When: boundary.solve(grid_out_of_range)
        pytest.fail("RED: U-FLOW-02d — range violation → E004 envelope, execute 0×")

    def test_u_flow_02e_duplicate_execute_zero_e005(self) -> None:
        # U-FLOW-02e
        # Given: duplicate non-zero; execute spied
        # boundary = UIBoundary()
        # When: boundary.solve(grid_duplicate)
        pytest.fail("RED: U-FLOW-02e — duplicate → E005 envelope, execute 0×")
