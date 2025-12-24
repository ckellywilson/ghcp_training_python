"""Unit tests for domain models."""

import pytest
from datetime import datetime
from domain.models import Airline


def test_airline_creation():
    """Test creating a valid airline."""
    airline = Airline(
        id="1",
        name="American Airlines",
        iata_code="AA",
        icao_code="AAL",
        country="United States"
    )
    
    assert airline.id == "1"
    assert airline.name == "American Airlines"
    assert airline.iata_code == "AA"
    assert airline.icao_code == "AAL"
    assert airline.country == "United States"
    assert airline.active is True


def test_airline_code_uppercase():
    """Test that airline codes are converted to uppercase."""
    airline = Airline(
        id="1",
        name="Delta",
        iata_code="dl",
        icao_code="dal",
        country="United States"
    )
    
    assert airline.iata_code == "DL"
    assert airline.icao_code == "DAL"


def test_airline_invalid_iata_code_length():
    """Test that invalid IATA code length raises ValueError."""
    with pytest.raises(ValueError, match="IATA code must be exactly 2 characters"):
        Airline(
            id="1",
            name="Test Airline",
            iata_code="ABC",
            icao_code="TEST",
            country="United States"
        )


def test_airline_empty_name():
    """Test that empty name raises ValueError."""
    with pytest.raises(ValueError, match="name cannot be empty"):
        Airline(
            id="1",
            name="",
            iata_code="AA",
            icao_code="AAL",
            country="United States"
        )


def test_airline_deactivate():
    """Test deactivating an airline."""
    airline = Airline(
        id="1",
        name="Test Airline",
        iata_code="TA",
        icao_code="TEST",
        country="Test Country"
    )
    
    assert airline.active is True
    deactivated = airline.deactivate()
    assert deactivated.active is False
    assert deactivated.updated_at is not None
    # Original instance remains unchanged (immutable)
    assert airline.active is True


def test_airline_activate():
    """Test activating an airline."""
    airline = Airline(
        id="1",
        name="Test Airline",
        iata_code="TA",
        icao_code="TEST",
        country="Test Country",
        active=False
    )
    
    assert airline.active is False
    activated = airline.activate()
    assert activated.active is True
    assert activated.updated_at is not None
    # Original instance remains unchanged (immutable)
    assert airline.active is False
