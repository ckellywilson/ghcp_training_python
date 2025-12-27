"""Common exceptions used across microservices."""

from typing import Any


class BaseServiceException(Exception):
    """Base exception for all service exceptions."""
    
    def __init__(self, message: str, details: dict[str, Any] | None = None):
        self.message = message
        self.details = details or {}
        super().__init__(self.message)


class ResourceNotFoundException(BaseServiceException):
    """Raised when a requested resource is not found."""
    pass


class ValidationException(BaseServiceException):
    """Raised when validation fails."""
    pass


class UnauthorizedException(BaseServiceException):
    """Raised when authentication or authorization fails."""
    pass


class ServiceUnavailableException(BaseServiceException):
    """Raised when a dependent service is unavailable."""
    pass


class ConflictException(BaseServiceException):
    """Raised when there's a conflict with existing data."""
    pass
