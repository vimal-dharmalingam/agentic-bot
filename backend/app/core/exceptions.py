class AppError(Exception):
    """Base class for all our custom errors."""


class LLMProviderError(AppError):
    """Raised when the LLM call fails."""


class RepositoryError(AppError):
    """Raised when the database call fails."""