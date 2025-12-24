"""Use cases for airline catalog operations."""

from datetime import datetime
from typing import Optional
import uuid

from domain.models import Airline
from domain.interfaces import AirlineRepository
from application.dtos import AirlineCreateDTO, AirlineUpdateDTO, AirlineResponseDTO


class CreateAirlineUseCase:
    """
    Use case for creating a new airline.
    
    Depends only on the domain interface, not concrete implementations.
    """
    
    def __init__(self, repository: AirlineRepository):
        """
        Initialize with airline repository.
        
        Args:
            repository: Repository implementation following AirlineRepository protocol
        """
        self.repository = repository
    
    def execute(self, dto: AirlineCreateDTO) -> AirlineResponseDTO:
        """
        Create a new airline in the catalog.
        
        Args:
            dto: Data transfer object with airline creation data
            
        Returns:
            Response DTO with created airline data
            
        Raises:
            ValueError: If airline with same code already exists
        """
        # Check if airline with this IATA code already exists
        existing = self.repository.find_by_iata_code(dto.iata_code.upper())
        if existing:
            raise ValueError(f"Airline with IATA code {dto.iata_code.upper()} already exists")
        
        # Check if airline with this ICAO code already exists
        existing_icao = self.repository.find_by_icao_code(dto.icao_code.upper())
        if existing_icao:
            raise ValueError(f"Airline with ICAO code {dto.icao_code.upper()} already exists")
        
        # Create domain entity
        airline = Airline(
            id=str(uuid.uuid4()),
            name=dto.name,
            iata_code=dto.iata_code,
            icao_code=dto.icao_code,
            country=dto.country,
            active=dto.active,
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
        
        # Persist
        self.repository.save(airline)
        
        # Return response DTO
        return AirlineResponseDTO.model_validate(airline)


class GetAirlineUseCase:
    """Use case for retrieving an airline by ID."""
    
    def __init__(self, repository: AirlineRepository):
        """Initialize with airline repository."""
        self.repository = repository
    
    def execute(self, airline_id: str) -> Optional[AirlineResponseDTO]:
        """
        Get an airline by ID.
        
        Args:
            airline_id: The unique identifier
            
        Returns:
            Response DTO if found, None otherwise
        """
        airline = self.repository.find_by_id(airline_id)
        if not airline:
            return None
        return AirlineResponseDTO.model_validate(airline)


class ListAirlinesUseCase:
    """Use case for listing airlines."""
    
    def __init__(self, repository: AirlineRepository):
        """Initialize with airline repository."""
        self.repository = repository
    
    def execute(self, active_only: bool = False) -> list[AirlineResponseDTO]:
        """
        List all airlines or only active ones.
        
        Args:
            active_only: If True, return only active airlines
            
        Returns:
            List of airline response DTOs
        """
        airlines = self.repository.find_active() if active_only else self.repository.find_all()
        return [AirlineResponseDTO.model_validate(airline) for airline in airlines]


class UpdateAirlineUseCase:
    """Use case for updating an airline."""
    
    def __init__(self, repository: AirlineRepository):
        """Initialize with airline repository."""
        self.repository = repository
    
    def execute(self, airline_id: str, dto: AirlineUpdateDTO) -> Optional[AirlineResponseDTO]:
        """
        Update an existing airline.
        
        Args:
            airline_id: The unique identifier
            dto: Data transfer object with update data
            
        Returns:
            Updated airline response DTO if found, None otherwise
        """
        airline = self.repository.find_by_id(airline_id)
        if not airline:
            return None
        
        # Create new instance with updated fields (immutable pattern)
        updated_airline = Airline(
            id=airline.id,
            name=dto.name if dto.name is not None else airline.name,
            iata_code=airline.iata_code,  # Codes cannot be updated
            icao_code=airline.icao_code,
            country=dto.country if dto.country is not None else airline.country,
            active=dto.active if dto.active is not None else airline.active,
            created_at=airline.created_at,
            updated_at=datetime.now()
        )
        
        # Persist changes
        self.repository.save(updated_airline)
        
        return AirlineResponseDTO.model_validate(updated_airline)


class DeleteAirlineUseCase:
    """Use case for deleting an airline."""
    
    def __init__(self, repository: AirlineRepository):
        """Initialize with airline repository."""
        self.repository = repository
    
    def execute(self, airline_id: str) -> bool:
        """
        Delete an airline by ID.
        
        Args:
            airline_id: The unique identifier
            
        Returns:
            True if deleted, False if not found
        """
        return self.repository.delete(airline_id)
