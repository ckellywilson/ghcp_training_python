# Python Language-Specific Instructions

These instructions apply to all Python code in this project.

## Python Version

- Use Python 3.11 or higher
- Leverage modern Python features (match statements, union types with `|`, etc.)

## Type System

### Type Hints
- **REQUIRED**: Use type hints for all function parameters and return values
- Use `Protocol` from `typing` for interface definitions (not ABC)
- Use Generic types where appropriate (`list[str]`, `dict[str, int]`)
- Prefer explicit types over `Any`
- Use union types with `|` syntax: `str | None` instead of `Optional[str]`

### Protocol for Interfaces
```python
from typing import Protocol

class Repository(Protocol):
    def find_by_id(self, id: str) -> Entity | None: ...
    def save(self, entity: Entity) -> None: ...
```

**Why Protocol over ABC:**
- Structural subtyping (duck typing with type safety)
- No need for explicit inheritance
- Better separation between interface and implementation

## Immutability Patterns

### Frozen Dataclasses for Domain Entities
**ALWAYS** use frozen dataclasses for domain entities and value objects:

```python
from dataclasses import dataclass

@dataclass(frozen=True)
class Airline:
    id: str
    name: str
    country: str
    
    def rename(self, new_name: str) -> 'Airline':
        """Return new instance with updated name."""
        return Airline(id=self.id, name=new_name, country=self.country)
```

**Benefits:**
- Thread-safety
- Prevents accidental mutation and validation bypass
- Predictable behavior
- Immutable by default

**Field Transformation:**
If you need to transform fields in `__post_init__`, use `object.__setattr__()`:
```python
@dataclass(frozen=True)
class Email:
    value: str
    
    def __post_init__(self):
        object.__setattr__(self, 'value', self.value.lower())
```

### Testing Immutable Entities
When testing immutable entities, assert that:
1. Methods return new instances
2. Original instances remain unchanged

```python
def test_rename_returns_new_instance():
    airline = Airline(id="1", name="Old", country="US")
    renamed = airline.rename("New")
    
    assert renamed.name == "New"
    assert airline.name == "Old"  # Original unchanged
    assert renamed is not airline  # Different instances
```

## Code Style

### PEP 8 Compliance
- Follow [PEP 8](https://peps.python.org/pep-0008/) style guidelines
- Use 4 spaces for indentation
- Maximum line length: 88 characters (Black formatter default)
- Use snake_case for variables and functions
- Use PascalCase for classes

### Documentation
- Use **Google-style docstrings** for public APIs and classes
- Document complex business logic with inline comments
- Include type information in docstrings when behavior is non-obvious

```python
def calculate_discount(price: float, rate: float) -> float:
    """Calculate the discounted price.
    
    Args:
        price: The original price before discount.
        rate: The discount rate as a decimal (0.1 = 10% off).
    
    Returns:
        The final price after applying the discount.
    
    Raises:
        ValueError: If rate is negative or greater than 1.
    """
    if not 0 <= rate <= 1:
        raise ValueError("Rate must be between 0 and 1")
    return price * (1 - rate)
```

### Naming Conventions
- Use descriptive variable and function names
- Avoid abbreviations unless widely understood
- Boolean variables should be predicates: `is_valid`, `has_items`, `can_process`
- Private attributes use single underscore: `_internal_state`

## Python Idioms

### Prefer Python Idioms
- Use comprehensions for simple transformations
- Use context managers for resource management
- Use early returns to reduce nesting
- Use `with` statements for file operations

```python
# Good: List comprehension
active_users = [u for u in users if u.is_active]

# Good: Early return
def process(value: str | None) -> str:
    if value is None:
        return ""
    return value.upper()

# Good: Context manager
with open('file.txt') as f:
    content = f.read()
```

### Avoid
- Bare `except:` clauses (always specify exception type)
- Mutable default arguments
- Using `*args` and `**kwargs` without clear purpose
- Global state

## Standard Library Usage

### Prefer Standard Library
- Use `dataclasses` for simple data containers
- Use `typing` for type hints and protocols
- Use `enum.Enum` for enumerated types
- Use `pathlib.Path` for file paths

### Collections
- Use `dict[K, V]` and `list[T]` for generic types (Python 3.9+)
- Use `collections.abc` for abstract base types when needed
- Use `typing.Protocol` for structural typing

## Design Patterns

### Composition Over Inheritance
- Favor composition and delegation over deep inheritance hierarchies
- Use Protocol to define interfaces instead of base classes
- Keep inheritance shallow (1-2 levels max)

### Single Responsibility Principle
- Keep functions small and focused (typically < 20 lines)
- Each function should do one thing well
- Extract complex logic into separate functions

## Error Handling

### Exception Definitions
- Define custom exceptions as needed
- Inherit from appropriate base exceptions
- Include helpful error messages

```python
class ValidationError(ValueError):
    """Raised when entity validation fails."""
    pass

class EntityNotFoundError(Exception):
    """Raised when an entity cannot be found."""
    def __init__(self, entity_type: str, entity_id: str):
        super().__init__(f"{entity_type} with id {entity_id} not found")
        self.entity_type = entity_type
        self.entity_id = entity_id
```

### Exception Handling
- Catch specific exceptions, not broad ones
- Re-raise with context when appropriate
- Log errors at the appropriate layer

## Testing Considerations

### Test Structure
- Use descriptive test names: `test_<method>_<scenario>_<expected_behavior>`
- Arrange-Act-Assert pattern
- One assertion per test (or related assertions)

### Fixtures and Mocks
- Use fixtures for shared test data
- Use protocols to enable easy mocking
- Prefer in-memory implementations for testing over mocks when possible
