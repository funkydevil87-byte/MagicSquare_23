from __future__ import annotations

from dataclasses import dataclass
from uuid import UUID


@dataclass(frozen=True, slots=True)
class User:
    """A user of the MagicSquare system.

    This entity represents a user identity and enforces basic domain invariants.

    Attributes:
        user_id: Unique identifier for the user.
        name: Display name for the user. Must be non-empty after trimming.
    """

    user_id: UUID
    name: str

    def __post_init__(self) -> None:
        """Validate domain invariants after initialization.

        Raises:
            ValueError: If `name` is empty or whitespace-only.
        """

        if self.name.strip() == "":
            raise ValueError("name must be non-empty")

    def rename(self, name: str) -> User:
        """Return a new User instance with an updated name.

        Args:
            name: New display name. Must be non-empty after trimming.

        Returns:
            A new immutable `User` instance with the updated name.

        Raises:
            ValueError: If `name` is empty or whitespace-only.
        """

        return User(user_id=self.user_id, name=name)

