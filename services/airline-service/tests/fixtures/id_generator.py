"""Test fixtures for ID generation."""


class DeterministicIdGenerator:
    """
    Deterministic ID generator for testing.
    
    Generates predictable IDs in sequence for easier test assertions.
    """
    
    def __init__(self, prefix: str = "test-id"):
        """
        Initialize with optional prefix.
        
        Args:
            prefix: Prefix for generated IDs
        """
        self.prefix = prefix
        self.counter = 0
    
    def generate(self) -> str:
        """
        Generate a deterministic ID.
        
        Returns:
            A predictable ID string in format: {prefix}-{counter}
        """
        self.counter += 1
        return f"{self.prefix}-{self.counter}"
