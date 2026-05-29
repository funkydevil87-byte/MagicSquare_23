"""MagicSquare domain entity layer."""

__all__ = ["User"]


def __getattr__(name: str) -> object:
    """Lazily expose entity public API to avoid import cycles."""
    if name == "User":
        from entity.user import User

        return User
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
