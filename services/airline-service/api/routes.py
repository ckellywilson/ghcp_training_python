"""FastAPI routes for airline catalog API."""

from fastapi import APIRouter, Depends, HTTPException, status
from typing import Annotated

from application.dtos import AirlineCreateDTO, AirlineUpdateDTO, AirlineResponseDTO
from application.use_cases import (
    CreateAirlineUseCase,
    GetAirlineUseCase,
    ListAirlinesUseCase,
    UpdateAirlineUseCase,
    DeleteAirlineUseCase
)
from api.di import (
    get_create_airline_use_case,
    get_get_airline_use_case,
    get_list_airlines_use_case,
    get_update_airline_use_case,
    get_delete_airline_use_case
)


router = APIRouter(prefix="/api/v1/airlines", tags=["airlines"])


@router.post("/", response_model=AirlineResponseDTO, status_code=status.HTTP_201_CREATED)
def create_airline(
    dto: AirlineCreateDTO,
    use_case: Annotated[CreateAirlineUseCase, Depends(get_create_airline_use_case)]
) -> AirlineResponseDTO:
    """
    Create a new airline in the catalog.
    
    Args:
        dto: Airline creation data
        use_case: Injected use case
        
    Returns:
        Created airline data
        
    Raises:
        HTTPException: 400 if airline with code already exists
    """
    try:
        return use_case.execute(dto)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get("/{airline_id}", response_model=AirlineResponseDTO)
def get_airline(
    airline_id: str,
    use_case: Annotated[GetAirlineUseCase, Depends(get_get_airline_use_case)]
) -> AirlineResponseDTO:
    """
    Get an airline by ID.
    
    Args:
        airline_id: Unique airline identifier
        use_case: Injected use case
        
    Returns:
        Airline data
        
    Raises:
        HTTPException: 404 if airline not found
    """
    result = use_case.execute(airline_id)
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Airline not found")
    return result


@router.get("/", response_model=list[AirlineResponseDTO])
def list_airlines(
    use_case: Annotated[ListAirlinesUseCase, Depends(get_list_airlines_use_case)],
    active_only: bool = False
) -> list[AirlineResponseDTO]:
    """
    List all airlines or only active ones.
    
    Args:
        active_only: If true, return only active airlines
        use_case: Injected use case
        
    Returns:
        List of airlines
    """
    return use_case.execute(active_only=active_only)


@router.put("/{airline_id}", response_model=AirlineResponseDTO)
def update_airline(
    airline_id: str,
    dto: AirlineUpdateDTO,
    use_case: Annotated[UpdateAirlineUseCase, Depends(get_update_airline_use_case)]
) -> AirlineResponseDTO:
    """
    Update an existing airline.
    
    Args:
        airline_id: Unique airline identifier
        dto: Update data
        use_case: Injected use case
        
    Returns:
        Updated airline data
        
    Raises:
        HTTPException: 404 if airline not found
    """
    result = use_case.execute(airline_id, dto)
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Airline not found")
    return result


@router.delete("/{airline_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_airline(
    airline_id: str,
    use_case: Annotated[DeleteAirlineUseCase, Depends(get_delete_airline_use_case)]
) -> None:
    """
    Delete an airline.
    
    Args:
        airline_id: Unique airline identifier
        use_case: Injected use case
        
    Raises:
        HTTPException: 404 if airline not found
    """
    success = use_case.execute(airline_id)
    if not success:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Airline not found")
