"""User domain entity (ECB entity layer)."""

from __future__ import annotations

from dataclasses import dataclass

# RFC 5321 path length guidance; practical upper bound for stored emails.
_MAX_EMAIL_LENGTH = 254
_MAX_DISPLAY_NAME_LENGTH = 120
_MIN_DISPLAY_NAME_LENGTH = 1


class InvalidUserError(ValueError):
    """Raised when ``User`` identity or profile invariants are violated."""


def _normalize_email(raw: str) -> str:
    """Return stripped, lowercased email for stable comparison.

    Args:
        raw: Raw email string from construction.

    Returns:
        Normalized email suitable for storage.

    Raises:
        InvalidUserError: If the string is empty after strip.
    """
    normalized = raw.strip().lower()
    if not normalized:
        msg = "email must not be empty"
        raise InvalidUserError(msg)
    return normalized


def _validate_email_shape(email: str) -> None:
    """Enforce minimal structural rules for an email address.

    Args:
        email: Normalized email (non-empty).

    Raises:
        InvalidUserError: If length or ``@`` placement is invalid.
    """
    if len(email) > _MAX_EMAIL_LENGTH:
        msg = f"email must be at most {_MAX_EMAIL_LENGTH} characters"
        raise InvalidUserError(msg)
    if email.count("@") != 1:
        msg = "email must contain exactly one '@' separator"
        raise InvalidUserError(msg)
    local, domain = email.split("@", 1)
    if not local or not domain:
        msg = "email local-part and domain must be non-empty"
        raise InvalidUserError(msg)
    if "." not in domain:
        msg = "email domain must contain a label separator ('.')"
        raise InvalidUserError(msg)


def _validate_display_name(raw: str) -> str:
    """Return stripped display name or raise.

    Args:
        raw: Candidate display name.

    Returns:
        Stripped display name.

    Raises:
        InvalidUserError: If length or emptiness is invalid.
    """
    name = raw.strip()
    if len(name) < _MIN_DISPLAY_NAME_LENGTH:
        msg = "display_name must not be empty"
        raise InvalidUserError(msg)
    if len(name) > _MAX_DISPLAY_NAME_LENGTH:
        msg = (
            f"display_name must be at most {_MAX_DISPLAY_NAME_LENGTH} characters"
        )
        raise InvalidUserError(msg)
    return name


def _validate_user_id(raw: str) -> str:
    """Return stripped external user identifier or raise.

    Args:
        raw: Stable unique id from the identity source.

    Returns:
        Stripped user id.

    Raises:
        InvalidUserError: If id is empty after strip.
    """
    user_id = raw.strip()
    if not user_id:
        msg = "user_id must not be empty"
        raise InvalidUserError(msg)
    return user_id


@dataclass(frozen=True)
class User:
    """Application user as a pure domain entity (no I/O, no framework types).

    Identity and profile fields are validated at construction. The aggregate
    is immutable; use ``rename`` to obtain a new instance with an updated
    display name.

    Attributes:
        user_id: Stable unique identifier (opaque string).
        email: Normalized (lowercased, stripped) email address.
        display_name: Non-empty human-readable label for UI.
    """

    user_id: str
    email: str
    display_name: str

    def __post_init__(self) -> None:
        """Validate invariants after field assignment.

        Raises:
            InvalidUserError: If any field violates domain rules.
        """
        object.__setattr__(self, "user_id", _validate_user_id(self.user_id))
        normalized = _normalize_email(self.email)
        _validate_email_shape(normalized)
        object.__setattr__(self, "email", normalized)
        object.__setattr__(
            self,
            "display_name",
            _validate_display_name(self.display_name),
        )

    def rename(self, new_display_name: str) -> User:
        """Return a new ``User`` with the same id and email, updated display name.

        Args:
            new_display_name: Replacement display name (trimmed, length-checked).

        Returns:
            New immutable ``User`` instance.

        Raises:
            InvalidUserError: If ``new_display_name`` is invalid.
        """
        return User(
            user_id=self.user_id,
            email=self.email,
            display_name=new_display_name,
        )
