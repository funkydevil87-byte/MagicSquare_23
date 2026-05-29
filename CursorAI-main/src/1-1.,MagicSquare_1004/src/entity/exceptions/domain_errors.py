"""Domain-level exception definitions."""


class DomainError(Exception):
    """Base exception for domain rule violations."""


class InvalidUserError(DomainError):
    """Raised when User entity invariants are violated."""
