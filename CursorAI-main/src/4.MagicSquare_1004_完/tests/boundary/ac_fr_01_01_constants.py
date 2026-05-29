"""AC-FR-01-01 contract constants shared by Boundary RED tests."""

AC_FR_01_01 = "AC-FR-01-01"
INVALID_SIZE_CODE = "INVALID_SIZE"
INVALID_SIZE_MESSAGE = "Grid must be 4x4."

EXCLUDED_AC_IDS = frozenset(
    {"AC-FR-01-02", "AC-FR-01-03", "AC-FR-01-04", "AC-FR-01-05"}
)
EXCLUDED_FR_IDS = frozenset({"FR-02", "FR-03", "FR-04", "FR-05"})

IN_SCOPE_SCENARIO_TAGS = frozenset({"null", "empty_list", "four_empty_rows", "size_3x4"})
FORBIDDEN_SCENARIO_TAGS = frozenset(
    {
        "empty_count_not_two",
        "out_of_range_value",
        "duplicate_nonzero",
        "valid_g1_grid",
        "domain_solve",
        "magic_square_validator",
    }
)
