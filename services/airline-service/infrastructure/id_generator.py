"""Concrete implementations of ID generator."""

import uuid


class UuidGenerator:
    """UUID-based ID generator implementation."""
    
    def generate(self) -> str:
        """Generate a UUID v4 identifier."""
        return str(uuid.uuid4())
