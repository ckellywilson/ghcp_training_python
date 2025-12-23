"""Domain entities for the airline catalog."""

from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class Airline:
    """
    Airline entity representing an airline in the catalog.
    
    This is a pure domain model with no framework dependencies.
    """
    id: str
    name: str
    code: str  # IATA code (e.g., "AA" for American Airlines)
    country: str
    active: bool = True
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    
    def __post_init__(self):
        """Validate airline data upon initialization."""
        if not self.code or len(self.code) != 2:
            raise ValueError("Airline code must be exactly 2 characters (IATA format)")
        if not self.name or not self.name.strip():
            raise ValueError("Airline name cannot be empty")
        if not self.country or not self.country.strip():
            raise ValueError("Country cannot be empty")
        
        # Ensure code is uppercase
        self.code = self.code.upper()
    
    def deactivate(self) -> None:
        """Deactivate this airline."""
        self.active = False
        self.updated_at = datetime.now()
    
    def activate(self) -> None:
        """Activate this airline."""
        self.active = True
        self.updated_at = datetime.now()
