# API Layer Instructions

Files in the `api/` directory handle HTTP concerns using the web framework.

## Route Definitions

- Use RESTful conventions: GET, POST, PUT, DELETE
- Include proper HTTP status codes in responses
- Use framework validation models for request/response validation
- Specify response types for automatic serialization

Example concept:
```
GET /users/{user_id} -> UserResponse (200)
    handler(user_id: string, use_case: GetUserUseCase):
        return use_case.execute(user_id)
```

## Dependency Injection

- Define provider functions in `api/di.py`
- Inject use cases, not repositories directly
- Use framework's dependency injection mechanism for all dependencies

Example concept:
```
get_user_repository() -> UserRepository:
    return SqlUserRepository(get_db_session())

get_user_use_case(repo: UserRepository) -> GetUserUseCase:
    return GetUserUseCase(repo)
```

## Error Handling

- Convert domain exceptions to HTTP responses
- Use framework exception handlers for consistent error responses
- Return appropriate status codes (400, 404, 500)

Example concept:
```
exception_handler(OrderNotFoundError):
    return JSONResponse(status_code=404, content={"detail": error.message})
```

## Response Models

- Use framework validation models for all responses
- Separate request and response models
- Use appropriate status codes
