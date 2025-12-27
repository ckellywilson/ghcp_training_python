# Project Overview

This project follows Clean Architecture principles. The project is designed to maintain clear separation of concerns, high testability, and independence from frameworks and external systems at the core business logic level.

## Architecture

This project follows Clean Architecture with strict layer boundaries:

### Layer Structure
- **Domain layer**: Pure business logic, entities, and interface definitions (ports)
  - Contains no framework or infrastructure dependencies
  - Defines business rules and domain models
  - Uses interfaces/protocols for all abstractions
- **Application layer**: DTOs and Use Case classes that depend only on Domain interfaces
  - Orchestrates domain logic
  - Remains framework-agnostic
  - Defines data transfer objects for communication
- **Infrastructure layer**: Concrete implementations of domain interfaces
  - Implements repositories, external services, and data access
  - Contains framework-specific code
  - Supports multiple implementations (e.g., SQL and InMemory repositories)
- **API layer**: HTTP routes and dependency injection wiring
  - Handles HTTP concerns (routing, serialization, validation)
  - Wires abstractions to implementations via dependency injection
- **Composition root**: Application entry point with DI configuration
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
│   ├── models.py          # Entities and value objects
│   └── interfaces.py      # Port/interface definitions
├── application/
│   ├── dtos.py           # Data Transfer Objects
│   └── use_cases.py      # Application use cases
├── infrastructure/
│   ├── repositories/     # Repository implementations
│   ├── services/         # External service implementations
│   └── database/         # Database-specific code
├── api/
│   ├── routes.py         # HTTP route definitions
│   └── di.py            # Dependency injection configuration
├── tests/
│   ├── unit/
│   ├── integration/
│   └── fixtures/
└── main.py               # Application entry point
```

## Dependency Injection

- Use framework-provided dependency injection mechanisms
- Define all DI wiring in the API layer's DI configuration
- Keep the composition root in the application entry point
- Inject interfaces, not concrete implementations, into use cases
- Make all dependencies explicit in function signatures

## Coding Standards

### Immutability Principles
- **Domain entities**: Should be immutable to prevent accidental mutation and validation bypass
  - Methods that modify state must return new instances
  - Ensures thread-safety and predictable behavior
  - Example pattern:
    ```
    class Airline:
        name: str
        
        def rename(self, new_name: str) -> 'Airline':
            return Airline(name=new_name)  # Return new instance
    ```
- **DTOs**: Should be immutable by default
- **Value objects**: Always immutable
- Benefits: Thread-safety, predictable behavior, prevents invalid state mutations

### Type Hints
- Use type hints for all function parameters and return values
- Use interfaces/protocols for abstractions
- Use generic types where appropriate
- Prefer explicit types over dynamic types

### Documentation
- Use language-appropriate docstring format for public APIs and classes
- Document complex business logic with inline comments
- Note architectural decisions in code comments where relevant

### Code Style
- Follow language-specific style guidelines
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
- Use framework validation models for request/response validation
- Handle errors consistently with proper exception handling
- Version your API endpoints when necessary

## Error Handling

- Define domain-specific exceptions in the domain layer
- Transform domain exceptions to HTTP responses in the API layer
- Use framework-provided exception handlers for consistent error responses
- Log errors appropriately at each layer

## Commit Message Standards

Follow Conventional Commits specification for all commits:

**Format**: `<type>(<scope>): <subject>`

**Types**:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting, no logic change)
- `refactor`: Code refactoring
- `test`: Adding or updating tests
- `chore`: Maintenance tasks (dependencies, build, config)

**Scopes** (use service name or layer):
- Service names: `airline-service`, `booking-service`, etc.
- Layers: `domain`, `application`, `infrastructure`, `api`
- Areas: `ci`, `docker`, `bicep`, `shared`

**Examples**:
- `feat(airline-service): add flight booking endpoint`
- `fix(domain): ensure airline entity immutability`
- `test(use-cases): add booking validation tests`
- `docs(readme): update Copilot configuration section`
- `refactor(infrastructure): extract repository base class`
- `chore(docker): update python base image to 3.11`

**Rules**:
- Keep subject line under 72 characters
- Use imperative mood ("add" not "added" or "adds")
- Don't capitalize first letter of subject
- No period at the end of subject
- Include scope when relevant
- Reference issue numbers in body when applicable (e.g., "Closes #123")
- Separate subject from body with blank line
- Use body to explain what and why, not how
