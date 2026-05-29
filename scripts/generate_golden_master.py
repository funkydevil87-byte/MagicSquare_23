#!/usr/bin/env python3
"""Generate tests/golden_master_expected.txt from live Magic Square Solver output."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from tests.golden_master_helper import (  # noqa: E402
    GOLDEN_MASTER_PATH,
    capture_all_scenarios,
    render_golden_master,
    write_golden_master,
)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Generate Golden Master baseline from solver output.",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=GOLDEN_MASTER_PATH,
        help=f"Output path (default: {GOLDEN_MASTER_PATH})",
    )
    parser.add_argument(
        "--stdout",
        action="store_true",
        help="Print generated content instead of writing a file.",
    )
    args = parser.parse_args()

    captures = capture_all_scenarios()
    content = render_golden_master(captures)

    if args.stdout:
        sys.stdout.write(content)
        return 0

    target = write_golden_master(args.output)
    print(f"Wrote Golden Master baseline: {target}")
    for key, capture in captures.items():
        label = "Output" if capture.kind == "success" else "Error"
        print(f"  [{key}] {label}: {capture.body}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
