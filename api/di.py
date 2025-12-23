"""Dependency injection configuration for FastAPI."""

from functools import lru_cache
from domain.interfaces import AirlineRepository
from infrastructure.repositories.in_memory_airline_repository import InMemoryAirlineRepository
from application.use_cases import (
    CreateAirlineUseCase,
    GetAirlineUseCase,
    ListAirlinesUseCase,
    UpdateAirlineUseCase,
    DeleteAirlineUseCase
)


# Singleton repository instance
_repository: AirlineRepository | None = None


def get_airline_repository() -> AirlineRepository:
    """
    Get airline repository instance.
    
    Uses in-memory implementation by default.
    In production, this would be configured to use a database implementation.
    """
    global _repository
    if _repository is None:
        _repository = InMemoryAirlineRepository()
    return _repository


def get_create_airline_use_case() -> CreateAirlineUseCase:
    """Dependency injection for CreateAirlineUseCase."""
    return CreateAirlineUseCase(get_airline_repository())


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
