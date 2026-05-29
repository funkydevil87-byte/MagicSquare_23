"""Tests for ``User`` entity invariants and behavior."""

import pytest

from magicsquare.entity.models.user import InvalidUserError, User


def test_user_creation_normalizes_email_and_strips_ids() -> None:
    """Valid construction lowercases email and strips whitespace."""
    # Arrange
    raw_id = "  usr-001  "
    raw_email = "  Alice.EXAMPLE@Sub.Domain.Com  "
    raw_name = "  Alice  "

    # Act
    user = User(user_id=raw_id, email=raw_email, display_name=raw_name)

    # Assert
    assert user.user_id == "usr-001"
    assert user.email == "alice.example@sub.domain.com"
    assert user.display_name == "Alice"


def test_user_rename_returns_new_instance_with_same_identity() -> None:
    """rename preserves id and email, updates display name only."""
    # Arrange
    original = User(
        user_id="u1",
        email="a@example.com",
        display_name="Old",
    )

    # Act
    renamed = original.rename("  New Name  ")

    # Assert
    assert renamed is not original
    assert renamed.user_id == original.user_id
    assert renamed.email == original.email
    assert renamed.display_name == "New Name"


def test_user_empty_user_id_raises() -> None:
    """Empty user_id violates identity invariant."""
    # Arrange
    invalid_id = "   "

    # Act / Assert
    with pytest.raises(InvalidUserError, match="user_id"):
        User(user_id=invalid_id, email="a@b.co", display_name="X")


def test_user_empty_email_raises() -> None:
    """Whitespace-only email is rejected."""
    # Arrange
    blank_email = "  \t  "

    # Act / Assert
    with pytest.raises(InvalidUserError, match="email"):
        User(user_id="u1", email=blank_email, display_name="X")


def test_user_email_without_single_at_raises() -> None:
    """Email must contain exactly one '@'."""
    # Arrange
    bad = "aliceexample.com"

    # Act / Assert
    with pytest.raises(InvalidUserError, match="@'"):
        User(user_id="u1", email=bad, display_name="X")


def test_user_email_missing_local_or_domain_raises() -> None:
    """Local part and domain must be non-empty around '@'."""
    # Arrange
    missing_domain = "onlylocal@"

    # Act / Assert
    with pytest.raises(InvalidUserError, match="local-part"):
        User(user_id="u1", email=missing_domain, display_name="X")


def test_user_email_domain_without_dot_raises() -> None:
    """Domain must include a dot (minimal structural rule)."""
    # Arrange
    bad = "a@localhost"

    # Act / Assert
    with pytest.raises(InvalidUserError, match="domain"):
        User(user_id="u1", email=bad, display_name="X")


def test_user_email_too_long_raises() -> None:
    """Email longer than maximum length is rejected."""
    # Arrange
    local = "a" * 200
    domain = "b" * 60
    long_email = f"{local}@{domain}.c"

    # Act / Assert
    with pytest.raises(InvalidUserError, match="at most"):
        User(user_id="u1", email=long_email, display_name="X")


def test_user_empty_display_name_raises() -> None:
    """Display name cannot be empty after strip."""
    # Arrange
    blank_name = "   "

    # Act / Assert
    with pytest.raises(InvalidUserError, match="display_name"):
        User(user_id="u1", email="a@b.co", display_name=blank_name)


def test_user_display_name_too_long_raises() -> None:
    """Display name over max length is rejected."""
    # Arrange
    too_long = "x" * 121

    # Act / Assert
    with pytest.raises(InvalidUserError, match="at most"):
        User(user_id="u1", email="a@b.co", display_name=too_long)


def test_user_rename_invalid_display_name_raises() -> None:
    """rename enforces the same display name rules as construction."""
    # Arrange
    user = User(user_id="u1", email="a@b.co", display_name="Ok")

    # Act / Assert
    with pytest.raises(InvalidUserError, match="display_name"):
        user.rename("")
