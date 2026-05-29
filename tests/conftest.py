"""Shared grid fixtures (G0~G3) — RED skeleton placeholders only."""

from __future__ import annotations

# G0 — complete 4×4 magic square (M=34); D-VAL-01~06 base
# GRID_G0: list[list[int]] = [
#     [16, 3, 2, 13],
#     [5, 10, 11, 8],
#     [9, 6, 7, 12],
#     [4, 15, 14, 1],
# ]

# G1 — Step A success; blanks (2,2),(3,3) 1-index; missing {7,10}; D-LOC/MIS/SOL-01/04
# GRID_G1: list[list[int]] = [
#     [16, 3, 2, 13],
#     [5, 0, 11, 8],
#     [9, 6, 0, 12],
#     [4, 15, 14, 1],
# ]

# G2 — Step B only (TD-02); blanks (1,1),(1,2); D-SOL-02 TBD until fixture locked
# GRID_G2: list[list[int]] = [
#     [0, 0, 2, 13],
#     [5, 10, 11, 8],
#     [9, 6, 7, 12],
#     [4, 15, 14, 1],
# ]

# G3 — both combinations fail; D-SOL-03 PLACEHOLDER (re-verify before GREEN)
# GRID_G3: list[list[int]] | None = None  # TBD
