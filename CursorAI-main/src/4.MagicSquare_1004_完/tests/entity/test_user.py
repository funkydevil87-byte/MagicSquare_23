"""Tests for the User domain entity."""

import pytest

from entity.exceptions.domain_errors import InvalidUserError
from entity.user import User


class TestUserCreation:
    """User entity creation and invariant validation."""

    def test_user_create_with_valid_fields(self) -> None:
        """Valid user_id and display_name produce a User instance."""
        # Arrange
        user_id = "user-001"
        display_name = "Alice"

        # Act
        user = User(user_id=user_id, display_name=display_name)

        # Assert
        assert user.user_id == "user-001"
        assert user.display_name == "Alice"

    def test_user_strips_surrounding_whitespace(self) -> None:
        """Leading and trailing whitespace is removed from fields."""
        # Arrange
        user_id = "  user-002  "
        display_name = "  Bob  "

        # Act
        user = User(user_id=user_id, display_name=display_name)

        # Assert
        assert user.user_id == "user-002"
        assert user.display_name == "Bob"

    @pytest.mark.parametrize(
        ("user_id", "display_name"),
        [
            ("", "Alice"),
            ("   ", "Alice"),
            ("user-001", ""),
            ("user-001", "   "),
        ],
    )
    def test_user_raises_when_required_field_is_blank(
        self, user_id: str, display_name: str
    ) -> None:
        """Blank user_id or display_name violates domain invariants."""
        # Arrange / Act / Assert
        with pytest.raises(InvalidUserError):
            User(user_id=user_id, display_name=display_name)

    def test_user_raises_when_display_name_exceeds_max_length(self) -> None:
        """Display name longer than MAX_DISPLAY_NAME_LENGTH is rejected."""
        # Arrange
        long_name = "A" * (User.MAX_DISPLAY_NAME_LENGTH + 1)

        # Act / Assert
        with pytest.raises(InvalidUserError):
            User(user_id="user-003", display_name=long_name)


class TestUserBehavior:
    """User entity behavior beyond construction."""

    def test_user_equality_based_on_fields(self) -> None:
        """Two Users with identical fields are equal."""
        # Arrange
        user_a = User(user_id="user-004", display_name="Carol")
        user_b = User(user_id="user-004", display_name="Carol")

        # Act / Assert
        assert user_a == user_b

    def test_user_inequality_when_fields_differ(self) -> None:
        """Users with different fields are not equal."""
        # Arrange
        user_a = User(user_id="user-005", display_name="Dave")
        user_b = User(user_id="user-006", display_name="Dave")

        # Act / Assert
        assert user_a != user_b

    def test_with_display_name_returns_new_instance(self) -> None:
        """with_display_name returns a new User without mutating the original."""
        # Arrange
        original = User(user_id="user-007", display_name="Eve")

        # Act
        updated = original.with_display_name("Eva")

        # Assert
        assert updated.display_name == "Eva"
        assert original.display_name == "Eve"
        assert updated.user_id == original.user_id
        assert updated is not original
