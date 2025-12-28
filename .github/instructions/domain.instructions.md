# Domain Layer Instructions

Files in the `domain/` directory contain pure business logic with no external dependencies.

## Core Principles

- **Zero Framework Dependencies**: No imports from web frameworks, validation libraries, or any infrastructure libraries
- **Interface-Based Abstractions**: All abstractions use language-appropriate interface mechanisms
- **Pure Business Logic**: Only standard library types and domain-specific classes

## Interface Definitions

Define interfaces for all repository and service abstractions that the domain needs.

Example concept:
```
interface OrderRepository:
    find_by_id(order_id: string) -> Order | null
    save(order: Order) -> void
```

## Domain Models

- Use immutable data structures for entities and value objects
- Implement business logic as methods on entities
- Keep validation logic within domain models
- Use value objects for complex types

## Domain Exceptions

Define domain-specific exceptions in this layer:

```
class OrderNotFoundError extends Exception:
    """Raised when an order cannot be found."""
```

## What NOT to Include

- ❌ Web framework dependencies
- ❌ Framework-specific validation models (use in application layer instead)
- ❌ Database models or ORM classes
- ❌ HTTP-specific code
- ❌ Concrete infrastructure implementations
