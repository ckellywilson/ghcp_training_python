"""Port definitions using Protocol for dependency inversion."""

from typing import Protocol, Optional
from domain.models import Airline


class IdGenerator(Protocol):
    """
    Interface for generating unique identifiers.
    
    Abstracts ID generation to improve testability and allow different
    ID generation strategies.
    """
    
    def generate(self) -> str:
        """
        Generate a unique identifier.
        
        Returns:
            A unique identifier string
        """
        ...


class AirlineRepository(Protocol):
    """
    Repository interface for Airline persistence.
    
    Uses Protocol for interface definition following project guidelines.
    Implementations must provide all methods defined here.
    """
    
    def find_by_id(self, airline_id: str) -> Optional[Airline]:
        """
        Find an airline by its unique identifier.
        
        Args:
            airline_id: The unique identifier of the airline
            
        Returns:
            The airline if found, None otherwise
        """
        ...
    
    def find_by_iata_code(self, iata_code: str) -> Optional[Airline]:
        """
        Find an airline by its IATA code.
        
        Args:
            iata_code: The IATA code (e.g., "AA")
            
        Returns:
            The airline if found, None otherwise
        """
        ...
    
    def find_by_icao_code(self, icao_code: str) -> Optional[Airline]:
        """
        Find an airline by its ICAO code.
        
        Args:
            icao_code: The ICAO code (e.g., "AAL")
            
        Returns:
            The airline if found, None otherwise
        """
        ...
    
    def find_all(self) -> list[Airline]:
        """
        Retrieve all airlines in the catalog.
        
        Returns:
            List of all airlines
        """
        ...
    
    def find_active(self) -> list[Airline]:
        """
        Retrieve all active airlines.
        
        Returns:
            List of active airlines
        """
        ...
    
    def save(self, airline: Airline) -> None:
        """
        Persist an airline (create or update).
        
        Args:
            airline: The airline to save
        """
        ...
    
    def delete(self, airline_id: str) -> bool:
        """
        Delete an airline by ID.
        
        Args:
            airline_id: The unique identifier of the airline
            
        Returns:
            True if deleted, False if not found
        """
        ...
