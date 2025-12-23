# Domain Layer Instructions

Files in the `domain/` directory contain pure business logic with no external dependencies.

## Core Principles

- **Zero Framework Dependencies**: No imports from FastAPI, Pydantic, or any infrastructure libraries
- **Protocol-Based Interfaces**: All abstractions use `Protocol` from `typing`, never ABC
- **Pure Python**: Only standard library types and domain-specific classes

## Interface Definitions

Use Protocol for all repository and service interfaces:

```python
from typing import Protocol

class OrderRepository(Protocol):
    def find_by_id(self, order_id: str) -> Order | None: ...
    def save(self, order: Order) -> None: ...
```

## Domain Models

- Use dataclasses or plain classes for entities
- Implement business logic as methods on entities
- Keep validation logic within domain models
- Use value objects for complex types

## Domain Exceptions

Define domain-specific exceptions in this layer:

```python
class OrderNotFoundError(Exception):
    """Raised when an order cannot be found."""
    pass
```

## What NOT to Include

- ❌ FastAPI dependencies
- ❌ Pydantic models (use in application layer instead)
- ❌ Database models or ORM classes
- ❌ HTTP-specific code
- ❌ Concrete infrastructure implementations
