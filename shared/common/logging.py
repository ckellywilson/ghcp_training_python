"""Logging configuration for microservices."""

import logging
import sys
from typing import Any

# Configure JSON logging format for structured logs
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"


def setup_logging(service_name: str, log_level: str = "INFO") -> logging.Logger:
    """
    Configure logging for a microservice.
    
    Args:
        service_name: Name of the service for log identification
        log_level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    
    Returns:
        Configured logger instance
    """
    logger = logging.getLogger(service_name)
    logger.setLevel(getattr(logging, log_level.upper()))
    
    # Console handler
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(getattr(logging, log_level.upper()))
    
    # Formatter
    formatter = logging.Formatter(LOG_FORMAT)
    handler.setFormatter(formatter)
    
    # Add handler if not already added
    if not logger.handlers:
        logger.addHandler(handler)
    
    return logger


def log_context(**kwargs: Any) -> dict[str, Any]:
    """
    Create a structured log context dictionary.
    
    Args:
        **kwargs: Key-value pairs for log context
    
    Returns:
        Dictionary with log context
    """
    return {"context": kwargs}
