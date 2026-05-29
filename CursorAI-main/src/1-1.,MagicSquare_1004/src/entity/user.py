"""User domain entity for MagicSquare application."""

from __future__ import annotations

from dataclasses import dataclass
from typing import ClassVar

from entity.exceptions.domain_errors import InvalidUserError


@dataclass(frozen=True, slots=True)
class User:
    """Domain entity representing a MagicSquare application user.

    Holds user identity and display metadata. Validation runs at construction
    time; instances are immutable.

    Attributes:
        user_id: Non-empty unique identifier for the user.
        display_name: Non-empty name shown in the application UI.
    """

    MAX_DISPLAY_NAME_LENGTH: ClassVar[int] = 50

    user_id: str
    display_name: str

    def __post_init__(self) -> None:
        """Normalize and validate fields after dataclass initialization."""
        normalized_user_id = self.user_id.strip()
        normalized_display_name = self.display_name.strip()
        object.__setattr__(self, "user_id", normalized_user_id)
        object.__setattr__(self, "display_name", normalized_display_name)
        self._validate()

    def _validate(self) -> None:
        """Validate domain invariants for user_id and display_name.

        Raises:
            InvalidUserError: If user_id or display_name violates invariants.
        """
        if not self.user_id:
            raise InvalidUserError("user_id must not be empty")
        if not self.display_name:
            raise InvalidUserError("display_name must not be empty")
        if len(self.display_name) > self.MAX_DISPLAY_NAME_LENGTH:
            raise InvalidUserError(
                f"display_name must not exceed {self.MAX_DISPLAY_NAME_LENGTH} characters"
            )

    def with_display_name(self, display_name: str) -> User:
        """Return a new User with an updated display name.

        Args:
            display_name: New display name; must satisfy the same invariants.

        Returns:
            A new User instance with the updated display_name.

        Raises:
            InvalidUserError: If display_name violates domain invariants.
        """
        return User(user_id=self.user_id, display_name=display_name)
