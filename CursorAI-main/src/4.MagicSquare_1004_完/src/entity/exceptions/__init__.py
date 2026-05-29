"""Domain exception types."""

__all__ = ["DomainError", "InvalidUserError"]


def __getattr__(name: str) -> object:
    """Lazily expose exception types to avoid import cycles."""
    if name in __all__:
        from entity.exceptions import domain_errors

        return getattr(domain_errors, name)
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
