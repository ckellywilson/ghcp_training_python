"""Dependency injection configuration for FastAPI."""

from functools import lru_cache
from domain.interfaces import AirlineRepository, IdGenerator
from infrastructure.repositories.in_memory_airline_repository import InMemoryAirlineRepository
from infrastructure.id_generator import UuidGenerator
from application.use_cases import (
    CreateAirlineUseCase,
    GetAirlineUseCase,
    ListAirlinesUseCase,
    UpdateAirlineUseCase,
    DeleteAirlineUseCase
)


@lru_cache
def get_airline_repository() -> AirlineRepository:
    """
    Get airline repository instance (singleton via lru_cache).
    
    Uses in-memory implementation by default.
    In production, this would be configured to use a database implementation.
    """
    return InMemoryAirlineRepository()


@lru_cache
def get_id_generator() -> IdGenerator:
    """
    Get ID generator instance (singleton via lru_cache).
    
    Uses UUID v4 implementation by default.
    """
    return UuidGenerator()


def get_create_airline_use_case() -> CreateAirlineUseCase:
    """Dependency injection for CreateAirlineUseCase."""
    return CreateAirlineUseCase(get_airline_repository(), get_id_generator())


def get_get_airline_use_case() -> GetAirlineUseCase:
    """Dependency injection for GetAirlineUseCase."""
    return GetAirlineUseCase(get_airline_repository())


def get_list_airlines_use_case() -> ListAirlinesUseCase:
    """Dependency injection for ListAirlinesUseCase."""
    return ListAirlinesUseCase(get_airline_repository())


def get_update_airline_use_case() -> UpdateAirlineUseCase:
    """Dependency injection for UpdateAirlineUseCase."""
    return UpdateAirlineUseCase(get_airline_repository())


def get_delete_airline_use_case() -> DeleteAirlineUseCase:
    """Dependency injection for DeleteAirlineUseCase."""
    return DeleteAirlineUseCase(get_airline_repository())
