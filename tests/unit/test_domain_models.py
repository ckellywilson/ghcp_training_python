"""Unit tests for domain models."""

import pytest
from datetime import datetime
from domain.models import Airline


def test_airline_creation():
    """Test creating a valid airline."""
    airline = Airline(
        id="1",
        name="American Airlines",
        code="AA",
        country="United States"
    )
    
    assert airline.id == "1"
    assert airline.name == "American Airlines"
    assert airline.code == "AA"
    assert airline.country == "United States"
    assert airline.active is True


def test_airline_code_uppercase():
    """Test that airline code is converted to uppercase."""
    airline = Airline(
        id="1",
        name="Delta",
        code="dl",
        country="United States"
    )
    
    assert airline.code == "DL"


def test_airline_invalid_code_length():
    """Test that invalid code length raises ValueError."""
    with pytest.raises(ValueError, match="must be exactly 2 characters"):
        Airline(
            id="1",
            name="Test Airline",
            code="ABC",
            country="United States"
        )


def test_airline_empty_name():
    """Test that empty name raises ValueError."""
    with pytest.raises(ValueError, match="name cannot be empty"):
        Airline(
            id="1",
            name="",
            code="AA",
            country="United States"
        )


def test_airline_deactivate():
    """Test deactivating an airline."""
    airline = Airline(
        id="1",
        name="Test Airline",
        code="TA",
        country="Test Country"
    )
    
    assert airline.active is True
    airline.deactivate()
    assert airline.active is False
    assert airline.updated_at is not None


def test_airline_activate():
    """Test activating an airline."""
    airline = Airline(
        id="1",
        name="Test Airline",
        code="TA",
        country="Test Country",
        active=False
    )
    
    assert airline.active is False
    airline.activate()
    assert airline.active is True
    assert airline.updated_at is not None
