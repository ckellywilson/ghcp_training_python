"""In-memory implementation of AirlineRepository for testing and development."""

from typing import Optional
from domain.models import Airline
from domain.interfaces import AirlineRepository


class InMemoryAirlineRepository:
    """
    In-memory implementation of AirlineRepository protocol.
    
    Useful for testing and development without external dependencies.
    """
    
    def __init__(self):
        """Initialize with empty storage."""
        self._airlines: dict[str, Airline] = {}
    
    def find_by_id(self, airline_id: str) -> Optional[Airline]:
        """Find airline by ID."""
        return self._airlines.get(airline_id)
    
    def find_by_iata_code(self, iata_code: str) -> Optional[Airline]:
        """Find airline by IATA code."""
        code_upper = iata_code.upper()
        for airline in self._airlines.values():
            if airline.iata_code == code_upper:
                return airline
        return None
    
    def find_by_icao_code(self, icao_code: str) -> Optional[Airline]:
        """Find airline by ICAO code."""
        code_upper = icao_code.upper()
        for airline in self._airlines.values():
            if airline.icao_code == code_upper:
                return airline
        return None
    
    def find_all(self) -> list[Airline]:
        """Get all airlines."""
        return list(self._airlines.values())
    
    def find_active(self) -> list[Airline]:
        """Get all active airlines."""
        return [airline for airline in self._airlines.values() if airline.active]
    
    def save(self, airline: Airline) -> None:
        """Save airline (create or update)."""
        self._airlines[airline.id] = airline
    
    def delete(self, airline_id: str) -> bool:
        """Delete airline by ID."""
        if airline_id in self._airlines:
            del self._airlines[airline_id]
            return True
        return False
    
    def clear(self) -> None:
        """Clear all airlines (useful for testing)."""
        self._airlines.clear()
