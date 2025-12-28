"""Common utilities package."""

from shared.common.exceptions import (
    BaseServiceException,
    ConflictException,
    ResourceNotFoundException,
    ServiceUnavailableException,
    UnauthorizedException,
    ValidationException,
)
from shared.common.logging import log_context, setup_logging
from shared.common.middleware import CorrelationIdMiddleware, RequestLoggingMiddleware

__all__ = [
    "BaseServiceException",
    "ResourceNotFoundException",
    "ValidationException",
    "UnauthorizedException",
    "ServiceUnavailableException",
    "ConflictException",
    "setup_logging",
    "log_context",
    "CorrelationIdMiddleware",
    "RequestLoggingMiddleware",
]
