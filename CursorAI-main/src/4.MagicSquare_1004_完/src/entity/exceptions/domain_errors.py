"""Domain-level exception definitions."""


class DomainError(Exception):
    """Base exception for domain rule violations."""


class InvalidUserError(DomainError):
    """Raised when User entity invariants are violated."""


class UnsolvableDomainError(DomainError):
    """Raised when neither Step A nor Step B yields a valid magic square."""


class InvalidGridStateError(DomainError):
    """Raised when grid state violates domain preconditions."""


class InvalidNumberSetError(DomainError):
    """Raised when present or missing number sets are invalid."""
