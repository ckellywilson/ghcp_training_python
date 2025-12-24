"""Integration tests for API endpoints."""

import pytest
from fastapi.testclient import TestClient
from main import create_app
from api.di import (
    get_airline_repository,
    get_create_airline_use_case,
    get_get_airline_use_case,
    get_list_airlines_use_case,
    get_update_airline_use_case,
    get_delete_airline_use_case
)
from application.use_cases import (
    CreateAirlineUseCase,
    GetAirlineUseCase,
    ListAirlinesUseCase,
    UpdateAirlineUseCase,
    DeleteAirlineUseCase
)
from infrastructure.repositories.in_memory_airline_repository import InMemoryAirlineRepository


@pytest.fixture
def client():
    """Create a test client with a fresh repository."""
    app = create_app()
    
    # Create fresh repository instance for each test
    test_repository = InMemoryAirlineRepository()
    
    # Override repository
    app.dependency_overrides[get_airline_repository] = lambda: test_repository
    
    # Override all use cases to use the test repository
    app.dependency_overrides[get_create_airline_use_case] = lambda: CreateAirlineUseCase(test_repository)
    app.dependency_overrides[get_get_airline_use_case] = lambda: GetAirlineUseCase(test_repository)
    app.dependency_overrides[get_list_airlines_use_case] = lambda: ListAirlinesUseCase(test_repository)
    app.dependency_overrides[get_update_airline_use_case] = lambda: UpdateAirlineUseCase(test_repository)
    app.dependency_overrides[get_delete_airline_use_case] = lambda: DeleteAirlineUseCase(test_repository)
    
    with TestClient(app) as test_client:
        yield test_client
    
    # Clean up dependency overrides
    app.dependency_overrides.clear()


def test_create_airline(client):
    """Test creating an airline via API."""
    response = client.post(
        "/api/v1/airlines/",
        json={
            "name": "American Airlines",
            "iata_code": "AA",
            "icao_code": "AAL",
            "country": "United States",
            "active": True
        }
    )
    
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "American Airlines"
    assert data["iata_code"] == "AA"
    assert data["icao_code"] == "AAL"
    assert data["id"] is not None


def test_create_duplicate_airline(client):
    """Test that creating duplicate airline code returns 400."""
    airline_data = {
        "name": "American Airlines",
        "iata_code": "AA",
        "icao_code": "AAL",
        "country": "United States"
    }
    
    # Create first airline
    response1 = client.post("/api/v1/airlines/", json=airline_data)
    assert response1.status_code == 201
    
    # Try to create duplicate
    response2 = client.post("/api/v1/airlines/", json=airline_data)
    assert response2.status_code == 400


def test_get_airline(client):
    """Test getting an airline by ID."""
    # Create airline
    create_response = client.post(
        "/api/v1/airlines/",
        json={"name": "Delta", "iata_code": "DL", "icao_code": "DAL", "country": "United States"}
    )
    airline_id = create_response.json()["id"]
    
    # Get airline
    response = client.get(f"/api/v1/airlines/{airline_id}")
    
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == airline_id
    assert data["name"] == "Delta"


def test_get_nonexistent_airline(client):
    """Test getting a non-existent airline returns 404."""
    response = client.get("/api/v1/airlines/nonexistent-id")
    assert response.status_code == 404


def test_list_airlines(client):
    """Test listing all airlines."""
    # Create multiple airlines
    client.post("/api/v1/airlines/", json={"name": "AA", "iata_code": "AA", "icao_code": "AAL", "country": "US"})
    client.post("/api/v1/airlines/", json={"name": "DL", "iata_code": "DL", "icao_code": "DAL", "country": "US"})
    
    # List all
    response = client.get("/api/v1/airlines/")
    
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2


def test_list_active_airlines_only(client):
    """Test listing only active airlines."""
    # Create active and inactive airlines
    client.post("/api/v1/airlines/", json={"name": "Active", "iata_code": "AC", "icao_code": "ACTV", "country": "US", "active": True})
    client.post("/api/v1/airlines/", json={"name": "Inactive", "iata_code": "IN", "icao_code": "INAC", "country": "US", "active": False})
    
    # List active only
    response = client.get("/api/v1/airlines/?active_only=true")
    
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["iata_code"] == "AC"


def test_update_airline(client):
    """Test updating an airline."""
    # Create airline
    create_response = client.post(
        "/api/v1/airlines/",
        json={"name": "United", "iata_code": "UA", "icao_code": "UAL", "country": "United States"}
    )
    airline_id = create_response.json()["id"]
    
    # Update airline
    response = client.put(
        f"/api/v1/airlines/{airline_id}",
        json={"name": "United Airlines", "active": False}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "United Airlines"
    assert data["active"] is False


def test_delete_airline(client):
    """Test deleting an airline."""
    # Create airline
    create_response = client.post(
        "/api/v1/airlines/",
        json={"name": "Test", "iata_code": "TS", "icao_code": "TEST", "country": "Test Country"}
    )
    airline_id = create_response.json()["id"]
    
    # Delete airline
    response = client.delete(f"/api/v1/airlines/{airline_id}")
    
    assert response.status_code == 204
    
    # Verify it's deleted
    get_response = client.get(f"/api/v1/airlines/{airline_id}")
    assert get_response.status_code == 404


def test_health_check(client):
    """Test health check endpoint."""
    response = client.get("/health")
    
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}
