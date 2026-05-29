"""Entity Track shared fixtures — G0~G3 grid placeholders (Report/02 부록).

Domain Mock 금지 (Dual-Track Logic Track).
"""

from __future__ import annotations

# G0 — 완전 유효 마방jin (D-VAL-01)
# grid_g0 = [[16,3,2,13],[5,10,11,8],[9,6,7,12],[4,15,14,1]]

# G1 — Step A 성공 (D-LOC-01, D-MIS-01, D-SOL-01)
# first=(2,2), second=(3,3), missing {7,10}
# grid_g1 = [[16,3,2,13],[5,0,11,8],[9,6,0,12],[4,15,14,1]]

# G2 — Step B만 성공 [TBD] (D-SOL-02)
# grid_g2 = ...  # Report/02 placeholder — RED 확정 전 TBD

# G3 — 무해 (D-SOL-03)
# first=(1,4), second=(2,3), missing {4,7}
# grid_g3 = [[1,2,3,0],[5,6,0,8],[9,10,11,12],[13,14,15,16]]
