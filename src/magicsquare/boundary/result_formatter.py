"""Format Boundary API success and failure payloads for callers."""

from __future__ import annotations

from typing import Any


class ResultFormatter:
    """Build ``int[6]`` vectors and user-facing result text."""

    @staticmethod
    def to_solution_vector(
        first_blank: tuple[int, int],
        second_blank: tuple[int, int],
        first_value: int,
        second_value: int,
    ) -> list[int]:
        """Return ``[r1, c1, n1, r2, c2, n2]`` with 1-indexed coordinates."""
        r1, c1 = first_blank
        r2, c2 = second_blank
        return [r1, c1, first_value, r2, c2, second_value]

    @staticmethod
    def format_validation_failure(code: str, message: str) -> str:
        return (
            "Boundary validation failed\n"
            f"  code: {code}\n"
            f"  message: {message}"
        )

    @staticmethod
    def format_unsolvable(code: str, message: str) -> str:
        return (
            "Boundary solve failed\n"
            f"  code: {code}\n"
            f"  message: {message}"
        )

    @staticmethod
    def format_success(result: list[int]) -> str:
        r1, c1, n1, r2, c2, n2 = result
        return (
            "Solve succeeded\n"
            f"  blank ({r1},{c1}) ← {n1}\n"
            f"  blank ({r2},{c2}) ← {n2}\n"
            f"  vector: {list(result)}"
        )

    @staticmethod
    def format_unknown(result: Any) -> str:
        return f"Unknown result type: {result!r}"
