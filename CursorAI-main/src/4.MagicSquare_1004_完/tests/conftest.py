"""Shared pytest configuration and fixtures."""

import sys
from pathlib import Path

SRC_PATH = Path(__file__).resolve().parent.parent / "src"
if str(SRC_PATH) not in sys.path:
    sys.path.insert(0, str(SRC_PATH))

pytest_plugins = ["tests.golden_master_conftest"]

# Report/02 G0~G3 grid placeholders (entity/conftest.py와 동일 SSOT)
#
# G0 — 완전 유효 마방jin (U-IN-04 Given, D-VAL-01)
# grid_g0 = [[16,3,2,13],[5,10,11,8],[9,6,7,12],[4,15,14,1]]
#
# G1 — Step A 성공 (U-OUT-01~03 Given, D-LOC/MIS/SOL)
# grid_g1 = [[16,3,2,13],[5,0,11,8],[9,6,0,12],[4,15,14,1]]
#
# G2 — Step B만 성공 [TBD] (D-SOL-02)
# grid_g2 = ...  # Report/02 placeholder
#
# G3 — 무해 (D-SOL-03)
# grid_g3 = [[1,2,3,0],[5,6,0,8],[9,10,11,12],[13,14,15,16]]
