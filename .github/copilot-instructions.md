# Project Overview

This is a Python FastAPI project following Clean Architecture principles. The project is designed to maintain clear separation of concerns, high testability, and independence from frameworks and external systems at the core business logic level.

## Python Version

- Use Python 3.11 or higher

## Architecture

This project follows Clean Architecture with strict layer boundaries:

### Layer Structure
- **Domain layer**: Pure business logic, Entities, and Protocol-based interfaces (ports)
  - Contains no framework or infrastructure dependencies
  - Defines business rules and domain models
  - Uses `Protocol` from `typing` for all interface definitions
- **Application layer**: DTOs and Use Case classes that depend only on Domain interfaces
  - Orchestrates domain logic
  - Remains framework-agnostic
  - Uses Pydantic models for DTOs
- **Infrastructure layer**: Concrete implementations of domain interfaces
  - Implements repositories, external services, and data access
  - Contains framework-specific code
  - Supports multiple implementations (e.g., SQL and InMemory repositories)
- **API layer**: FastAPI routes and dependency injection wiring
  - Handles HTTP concerns (routing, serialization, validation)
  - Wires abstractions to implementations via dependency injection
- **Composition root**: main.py with DI configuration
  - Builds the complete object graph
  - Configures application startup

### Dependency Rules
- Domain and Application layers must NOT depend on frameworks, databases, or external systems
- Dependencies point inward: API → Application → Domain
- Outer layers depend on inner layers, never the reverse
- Use dependency inversion to allow outer layers to implement inner layer interfaces

## Folder Structure

```
project-root/
├── domain/
│   ├── __init__.py
│   ├── models.py          # Entities and value objects
│   └── interfaces.py      # Protocol-based port definitions
├── application/
│   ├── __init__.py
│   ├── dtos.py           # Data Transfer Objects (Pydantic models)
│   └── use_cases.py      # Application use cases
├── infrastructure/
│   ├── __init__.py
│   ├── repositories/     # Repository implementations
│   ├── services/         # External service implementations
│   └── database/         # Database-specific code
├── api/
│   ├── __init__.py
│   ├── routes.py         # FastAPI route definitions
│   └── di.py            # Dependency injection configuration
├── tests/
│   ├── unit/
│   ├── integration/
│   └── fixtures/
├── main.py               # Application entry point
├── requirements.txt
└── README.md
```

## Framework and Libraries

- **FastAPI** (v0.104.0+) for the web framework
- **Pydantic** (v2.0+) for data validation and DTOs
- **uvicorn** for the ASGI server
- **Protocol** from `typing` for interface definitions (not ABC)

### Protocol Example
```python
from typing import Protocol

class UserRepository(Protocol):
    def find_by_id(self, user_id: str) -> User | None: ...
    def save(self, user: User) -> None: ...
```

## Dependency Injection

- Use FastAPI's `Depends` for dependency injection
- Define all DI wiring in `api/di.py`
- Keep the composition root in `main.py`
- Inject interfaces, not concrete implementations, into use cases
- Make all dependencies explicit in function signatures

## Coding Standards

### Immutability Principles
- **Domain entities**: ALWAYS use frozen dataclasses (`@dataclass(frozen=True)`)
  - Prevents accidental mutation and validation bypass
  - Methods that modify state must return new instances
  - Use `object.__setattr__()` in `__post_init__` if field transformation is needed
  - Example:
    ```python
    @dataclass(frozen=True)
    class Airline:
        name: str
        
        def rename(self, new_name: str) -> 'Airline':
            return Airline(name=new_name)  # Return new instance
    ```
- **DTOs**: Pydantic models are immutable by default (no additional configuration needed)
- **Value objects**: Always immutable, use frozen dataclasses
- Benefits: Thread-safety, predictable behavior, prevents invalid state mutations

### Type Hints
- Use type hints for all function parameters and return values
- Use Protocol for interface definitions
- Use Generic types where appropriate
- Prefer explicit types over Any

### Documentation
- Use Google-style docstrings for public APIs and classes
- Document complex business logic with inline comments
- Note architectural decisions in code comments where relevant

### Code Style
- Follow PEP 8 style guidelines
- Use descriptive variable and function names
- Keep functions small and focused (Single Responsibility Principle)
- Prefer composition over inheritance
- Use early returns to reduce nesting

### SOLID Principles
- **Single Responsibility**: Each class should have one reason to change
- **Open/Closed**: Open for extension, closed for modification
- **Liskov Substitution**: Subtypes must be substitutable for their base types
- **Interface Segregation**: Many specific interfaces over one general interface
- **Dependency Inversion**: Depend on abstractions, not concretions

## Testing

- Write unit tests for domain and application layers
- Write integration tests for infrastructure layer
- Write API tests for the API layer
- Use in-memory implementations for testing use cases
- Mock external dependencies in tests
- Aim for high test coverage, especially in domain logic
- **When testing immutable entities**: Assert that methods return new instances and original instances remain unchanged

## API Design

- Use RESTful conventions for endpoint naming
- Return appropriate HTTP status codes
- Use Pydantic models for request/response validation
- Handle errors consistently with proper exception handling
- Version your API endpoints when necessary

## Error Handling

- Define domain-specific exceptions in the domain layer
- Transform domain exceptions to HTTP responses in the API layer
- Use FastAPI's exception handlers for consistent error responses
- Log errors appropriately at each layer
