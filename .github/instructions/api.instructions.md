# API Layer Instructions

Files in the `api/` directory handle HTTP concerns using FastAPI.

## Route Definitions

- Use RESTful conventions: GET, POST, PUT, DELETE
- Include proper HTTP status codes in responses
- Use Pydantic models for request/response validation
- Add response_model to endpoints for automatic serialization

```python
@router.get("/users/{user_id}", response_model=UserResponse, status_code=200)
async def get_user(user_id: str, use_case: GetUserUseCase = Depends(get_user_use_case)):
    return use_case.execute(user_id)
```

## Dependency Injection

- Define provider functions in `api/di.py`
- Inject use cases, not repositories directly
- Use FastAPI's `Depends()` for all dependencies

```python
def get_user_repository() -> UserRepository:
    return SqlUserRepository(get_db_session())

def get_user_use_case(
    repo: UserRepository = Depends(get_user_repository)
) -> GetUserUseCase:
    return GetUserUseCase(repo)
```

## Error Handling

- Convert domain exceptions to HTTP responses
- Use FastAPI exception handlers for consistent error responses
- Return appropriate status codes (400, 404, 500)

```python
@app.exception_handler(OrderNotFoundError)
async def order_not_found_handler(request: Request, exc: OrderNotFoundError):
    return JSONResponse(status_code=404, content={"detail": str(exc)})
```

## Response Models

- Use Pydantic models for all responses
- Separate request and response models
- Use appropriate status codes with status_code parameter
