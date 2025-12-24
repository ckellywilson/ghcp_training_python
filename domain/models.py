"""Domain entities for the airline catalog."""

from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass(frozen=True)
class Airline:
    """
    Airline entity representing an airline in the catalog.
    
    This is a pure domain model with no framework dependencies.
    """
    id: str
    name: str
    iata_code: str  # IATA code (e.g., "AA" for American Airlines)
    icao_code: str  # ICAO code (e.g., "AAL" for American Airlines)
    country: str
    active: bool = True
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    
    def __post_init__(self):
        """Validate airline data upon initialization."""
        if not self.iata_code or len(self.iata_code) != 2:
            raise ValueError("IATA code must be exactly 2 characters")
        if not self.icao_code or len(self.icao_code) < 3 or len(self.icao_code) > 4:
            raise ValueError("ICAO code must be 3 or 4 characters")
        if not self.name or not self.name.strip():
            raise ValueError("Airline name cannot be empty")
        if not self.country or not self.country.strip():
            raise ValueError("Country cannot be empty")
        
        # Ensure codes are uppercase (using object.__setattr__ since dataclass is frozen)
        object.__setattr__(self, 'iata_code', self.iata_code.upper())
        object.__setattr__(self, 'icao_code', self.icao_code.upper())
    
    def deactivate(self) -> 'Airline':
        """Return a new deactivated airline instance."""
        return Airline(
            id=self.id,
            name=self.name,
            iata_code=self.iata_code,
            icao_code=self.icao_code,
            country=self.country,
            active=False,
            created_at=self.created_at,
            updated_at=datetime.now()
        )
    
    def activate(self) -> 'Airline':
        """Return a new activated airline instance."""
        return Airline(
            id=self.id,
            name=self.name,
            iata_code=self.iata_code,
            icao_code=self.icao_code,
            country=self.country,
            active=True,
            created_at=self.created_at,
            updated_at=datetime.now()
        )
