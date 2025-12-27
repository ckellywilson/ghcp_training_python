# FastAPI Framework Instructions

These instructions apply to FastAPI-specific code in the API layer.

## Framework Versions

- **FastAPI** (v0.104.0+)
- **Pydantic** (v2.0+) for data validation and DTOs
- **uvicorn** for the ASGI server

## Pydantic Models

### DTOs with Pydantic
All DTOs in the application layer should use Pydantic models:

```python
from pydantic import BaseModel, Field

class CreateAirlineRequest(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    country: str = Field(..., min_length=2, max_length=2)
    
    model_config = {
        "json_schema_extra": {
            "examples": [{
                "name": "Delta Airlines",
                "country": "US"
            }]
        }
    }

class AirlineResponse(BaseModel):
    id: str
    name: str
    country: str
```

### Pydantic V2 Features
- Use `model_config` instead of `Config` class
- Use `Field()` for validation and metadata
- DTOs are immutable by default (no additional configuration needed)
- Use `model_validate()` instead of `parse_obj()`

## Dependency Injection

### FastAPI's Depends
- Use `Depends()` for all dependency injection
- Define provider functions in `api/di.py`
- Keep the composition root in `main.py`

```python
# api/di.py
from fastapi import Depends

def get_airline_repository() -> AirlineRepository:
    # In production, return database implementation
    return InMemoryAirlineRepository()

def get_create_airline_use_case(
    repository: AirlineRepository = Depends(get_airline_repository),
    id_generator: IdGenerator = Depends(get_id_generator)
) -> CreateAirlineUseCase:
    return CreateAirlineUseCase(repository, id_generator)
```

### Dependency Injection Patterns
- Inject use cases into route handlers, not repositories directly
- Make all dependencies explicit in function signatures
- Use type hints for dependency resolution
- Inject interfaces (Protocols), not concrete implementations

## Route Definitions

### RESTful Endpoint Patterns
```python
from fastapi import APIRouter, Depends, HTTPException, status

router = APIRouter(prefix="/airlines", tags=["airlines"])

@router.post("/", response_model=AirlineResponse, status_code=status.HTTP_201_CREATED)
async def create_airline(
    request: CreateAirlineRequest,
    use_case: CreateAirlineUseCase = Depends(get_create_airline_use_case)
) -> AirlineResponse:
    """Create a new airline."""
    result = use_case.execute(CreateAirlineDTO(**request.model_dump()))
    return AirlineResponse(**result.model_dump())

@router.get("/{airline_id}", response_model=AirlineResponse)
async def get_airline(
    airline_id: str,
    use_case: GetAirlineUseCase = Depends(get_get_airline_use_case)
) -> AirlineResponse:
    """Get an airline by ID."""
    try:
        result = use_case.execute(airline_id)
        return AirlineResponse(**result.model_dump())
    except AirlineNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
```

### HTTP Status Codes
Use appropriate status codes:
- `200 OK`: Successful GET, PUT, PATCH
- `201 Created`: Successful POST
- `204 No Content`: Successful DELETE
- `400 Bad Request`: Validation errors
- `404 Not Found`: Resource not found
- `409 Conflict`: Business rule violation
- `500 Internal Server Error`: Unexpected errors

### Response Models
- Always specify `response_model` for type safety and documentation
- Use `status_code` parameter for non-200 success responses
- Separate request and response models

## Error Handling

### Exception Handlers
Convert domain exceptions to HTTP responses:

```python
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

app = FastAPI()

@app.exception_handler(AirlineNotFoundError)
async def airline_not_found_handler(request: Request, exc: AirlineNotFoundError):
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={"detail": str(exc)}
    )

@app.exception_handler(ValidationError)
async def validation_error_handler(request: Request, exc: ValidationError):
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"detail": str(exc)}
    )
```

### HTTPException
Use `HTTPException` directly in route handlers for HTTP-specific errors:

```python
from fastapi import HTTPException, status

if not user.is_authorized():
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="User not authorized to perform this action"
    )
```

## Application Configuration

### Main Application Setup
```python
# main.py
from fastapi import FastAPI
from api.routes import router

app = FastAPI(
    title="Airline Service API",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Include routers
app.include_router(router)

# Register exception handlers
app.add_exception_handler(AirlineNotFoundError, airline_not_found_handler)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

### CORS Configuration
```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

## API Versioning

### URL Path Versioning
```python
router_v1 = APIRouter(prefix="/api/v1")
router_v2 = APIRouter(prefix="/api/v2")

app.include_router(router_v1)
app.include_router(router_v2)
```

## Request Validation

### Path Parameters
```python
@router.get("/airlines/{airline_id}")
async def get_airline(airline_id: str = Path(..., min_length=1)):
    pass
```

### Query Parameters
```python
from fastapi import Query

@router.get("/airlines")
async def list_airlines(
    country: str | None = Query(None, min_length=2, max_length=2),
    limit: int = Query(10, ge=1, le=100)
):
    pass
```

### Request Body
```python
@router.post("/airlines")
async def create_airline(request: CreateAirlineRequest):
    # Pydantic automatically validates the request body
    pass
```

## Testing FastAPI Applications

### Test Client
```python
from fastapi.testclient import TestClient

client = TestClient(app)

def test_create_airline():
    response = client.post(
        "/airlines",
        json={"name": "Test Airline", "country": "US"}
    )
    assert response.status_code == 201
    assert response.json()["name"] == "Test Airline"
```

## Background Tasks

### For Long-Running Operations
```python
from fastapi import BackgroundTasks

@router.post("/process")
async def process_data(background_tasks: BackgroundTasks):
    background_tasks.add_task(process_in_background, data)
    return {"message": "Processing started"}
```

## Best Practices

### Keep Routes Thin
- Route handlers should only handle HTTP concerns
- Delegate business logic to use cases
- Convert between HTTP models and DTOs at the API boundary

### Async vs Sync
- Use `async def` for I/O-bound operations
- Use regular `def` for CPU-bound operations
- Don't mix blocking code in async functions

### Documentation
- Use docstrings for route handlers (appears in OpenAPI docs)
- Provide examples in Pydantic models
- Document all parameters with `Field()` descriptions
