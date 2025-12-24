"""Data Transfer Objects using Pydantic for validation."""

from pydantic import BaseModel, ConfigDict, Field
from datetime import datetime
from typing import Optional


class AirlineCreateDTO(BaseModel):
    """DTO for creating a new airline."""
    name: str = Field(..., min_length=1, description="Airline name")
    code: str = Field(..., min_length=2, max_length=2, description="IATA airline code")
    country: str = Field(..., min_length=1, description="Country of origin")
    active: bool = Field(default=True, description="Whether the airline is active")


class AirlineUpdateDTO(BaseModel):
    """DTO for updating an existing airline."""
    name: Optional[str] = Field(None, min_length=1, description="Airline name")
    country: Optional[str] = Field(None, min_length=1, description="Country of origin")
    active: Optional[bool] = Field(None, description="Whether the airline is active")


class AirlineResponseDTO(BaseModel):
    """DTO for airline responses."""
    model_config = ConfigDict(from_attributes=True)
    
    id: str
    name: str
    code: str
    country: str
    active: bool
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
