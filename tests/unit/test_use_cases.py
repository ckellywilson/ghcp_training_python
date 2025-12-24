"""Unit tests for use cases."""

import pytest
from application.use_cases import CreateAirlineUseCase, GetAirlineUseCase, ListAirlinesUseCase
from application.dtos import AirlineCreateDTO
from infrastructure.repositories.in_memory_airline_repository import InMemoryAirlineRepository


@pytest.fixture
def repository():
    """Provide a fresh repository for each test."""
    return InMemoryAirlineRepository()


def test_create_airline_use_case(repository):
    """Test creating an airline through the use case."""
    use_case = CreateAirlineUseCase(repository)
    dto = AirlineCreateDTO(
        name="American Airlines",
        iata_code="AA",
        icao_code="AAL",
        country="United States"
    )
    
    result = use_case.execute(dto)
    
    assert result.name == "American Airlines"
    assert result.iata_code == "AA"
    assert result.icao_code == "AAL"
    assert result.country == "United States"
    assert result.active is True
    assert result.id is not None


def test_create_duplicate_airline_code(repository):
    """Test that creating an airline with duplicate code raises ValueError."""
    use_case = CreateAirlineUseCase(repository)
    dto = AirlineCreateDTO(
        name="American Airlines",
        iata_code="AA",
        icao_code="AAL",
        country="United States"
    )
    
    # Create first airline
    use_case.execute(dto)
    
    # Try to create duplicate
    with pytest.raises(ValueError, match="already exists"):
        use_case.execute(dto)


def test_get_airline_use_case(repository):
    """Test getting an airline by ID."""
    create_use_case = CreateAirlineUseCase(repository)
    get_use_case = GetAirlineUseCase(repository)
    
    # Create airline
    dto = AirlineCreateDTO(
        name="Delta",
        iata_code="DL",
        icao_code="DAL",
        country="United States"
    )
    created = create_use_case.execute(dto)
    
    # Get airline
    result = get_use_case.execute(created.id)
    
    assert result is not None
    assert result.id == created.id
    assert result.name == "Delta"


def test_get_nonexistent_airline(repository):
    """Test getting a non-existent airline returns None."""
    use_case = GetAirlineUseCase(repository)
    result = use_case.execute("nonexistent-id")
    
    assert result is None


def test_list_airlines_use_case(repository):
    """Test listing all airlines."""
    create_use_case = CreateAirlineUseCase(repository)
    list_use_case = ListAirlinesUseCase(repository)
    
    # Create multiple airlines
    dto1 = AirlineCreateDTO(name="American Airlines", iata_code="AA", icao_code="AAL", country="United States")
    dto2 = AirlineCreateDTO(name="Delta", iata_code="DL", icao_code="DAL", country="United States")
    
    create_use_case.execute(dto1)
    create_use_case.execute(dto2)
    
    # List all
    results = list_use_case.execute(active_only=False)
    
    assert len(results) == 2
    assert any(r.iata_code == "AA" for r in results)
    assert any(r.iata_code == "DL" for r in results)


def test_list_active_airlines_only(repository):
    """Test listing only active airlines."""
    create_use_case = CreateAirlineUseCase(repository)
    list_use_case = ListAirlinesUseCase(repository)
    
    # Create active and inactive airlines
    dto_active = AirlineCreateDTO(name="Active", iata_code="AC", icao_code="ACTV", country="US", active=True)
    dto_inactive = AirlineCreateDTO(name="Inactive", iata_code="IN", icao_code="INAC", country="US", active=False)
    
    create_use_case.execute(dto_active)
    create_use_case.execute(dto_inactive)
    
    # List active only
    results = list_use_case.execute(active_only=True)
    
    assert len(results) == 1
    assert results[0].iata_code == "AC"
