"""RF-05 — ResultFormatter SSOT for Boundary success/failure display."""

from __future__ import annotations

from magicsquare.boundary.result_formatter import ResultFormatter


class TestToSolutionVector:
    """RF-05-01 — int[6] vector assembly."""

    def test_to_solution_vector_one_indexed(self) -> None:
        vector = ResultFormatter.to_solution_vector((2, 2), (3, 3), 7, 10)
        assert vector == [2, 2, 7, 3, 3, 10]


class TestFormatValidationFailure:
    def test_includes_code_and_message(self) -> None:
        text = ResultFormatter.format_validation_failure(
            "NULL_INPUT",
            "Input matrix must not be null.",
        )
        assert "Boundary validation failed" in text
        assert "NULL_INPUT" in text
        assert "Input matrix must not be null." in text


class TestFormatUnsolvable:
    def test_includes_unsolvable_code(self) -> None:
        text = ResultFormatter.format_unsolvable("UNSOLVABLE", "No valid combination.")
        assert "Boundary solve failed" in text
        assert "UNSOLVABLE" in text
        assert "No valid combination." in text


class TestFormatSuccess:
    def test_includes_coordinates_and_vector(self) -> None:
        text = ResultFormatter.format_success([2, 2, 10, 3, 3, 7])
        assert "Solve succeeded" in text
        assert "blank (2,2) ← 10" in text
        assert "[2, 2, 10, 3, 3, 7]" in text


class TestFormatUnknown:
    def test_unknown_result_type(self) -> None:
        text = ResultFormatter.format_unknown({"unexpected": True})
        assert "Unknown result type" in text
