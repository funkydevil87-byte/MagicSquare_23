"""D-SOL-01~04 — SolvePartialMagicSquare / solution vector. Track B Control RED skeleton."""

from __future__ import annotations

import pytest


class TestDSol01StepA:
    """D-SOL-01 — G1 small-first success vector."""

    def test_d_sol_01_g1_step_a_vector(self) -> None:
        # D-SOL-01
        # from magicsquare.control.solve_partial_magic_square import SolvePartialMagicSquare
        # Given: G1 partial grid
        # solver = SolvePartialMagicSquare()
        # When: solver.execute(grid_g1) or solve pipeline
        pytest.fail("RED: D-SOL-01 — G1 returns [2,2,7,3,3,10] Step A (I8)")


class TestDSol02StepB:
    """D-SOL-02 — G2 reverse-only success (fixture TBD)."""

    def test_d_sol_02_g2_reverse_vector(self) -> None:
        # D-SOL-02
        # from magicsquare.control.solve_partial_magic_square import SolvePartialMagicSquare
        # Given: G2 (TD-02) partial grid; design lock [1,1,16,1,2,3]
        # solver = SolvePartialMagicSquare()
        # When: solver.execute(grid_g2)
        pytest.fail("RED: D-SOL-02 — G2 TBD")


class TestDSol03Unsolvable:
    """D-SOL-03 — G3 both combinations fail."""

    def test_d_sol_03_g3_unsolvable_domain_error(self) -> None:
        # D-SOL-03
        # from magicsquare.control.solve_partial_magic_square import SolvePartialMagicSquare
        # Given: G3 placeholder grid (both attempts invalid)
        # solver = SolvePartialMagicSquare()
        # When: solver.execute(grid_g3)
        pytest.fail("RED: D-SOL-03 — G3 raises UnsolvableDomainError (I10)")


class TestDSol04OutputShape:
    """D-SOL-04 — G1 output contract (len=6, 1-index)."""

    def test_d_sol_04_g1_output_length_and_indexing(self) -> None:
        # D-SOL-04
        # from magicsquare.control.solve_partial_magic_square import SolvePartialMagicSquare
        # Given: G1 partial grid
        # solver = SolvePartialMagicSquare()
        # When: solver.execute(grid_g1) → int[6]
        pytest.fail("RED: D-SOL-04 — G1 solution len=6, coords 1-index (I8, BR-14/15)")
