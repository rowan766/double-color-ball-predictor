class AppError(Exception):
    """Base exception for application-level errors."""


class NotFoundError(AppError):
    """Raised when a requested entity does not exist."""
