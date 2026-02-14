class AppError(Exception):
    """Base exception for application errors."""
    pass

class resourceNotFound(AppError):
    """Resource not found error."""
    pass

class ServiceUnavailable(AppError):
    """External service unavailable error."""
    pass

class ValidationError(AppError):
    """Data validation error."""
    pass
