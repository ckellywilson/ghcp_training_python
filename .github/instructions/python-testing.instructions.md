# Python Testing Instructions

These instructions apply to all test code in the project.

## Testing Framework

- Use **pytest** as the primary testing framework
- Use **pytest-asyncio** for testing async code
- Use **pytest-cov** for coverage reporting

## Test Organization

### Directory Structure
```
tests/
├── __init__.py
├── fixtures/          # Shared test fixtures and factories
│   ├── __init__.py
│   └── factories.py
├── unit/             # Unit tests (domain + application)
│   ├── __init__.py
│   ├── test_domain_models.py
│   └── test_use_cases.py
├── integration/      # Integration tests (infrastructure)
│   ├── __init__.py
│   ├── test_repositories.py
│   └── test_api.py
└── conftest.py       # Shared pytest configuration and fixtures
```

### Test File Naming
- Test files: `test_*.py` or `*_test.py`
- Test functions: `test_<function>_<scenario>_<expected_outcome>`
- Test classes: `Test<ClassName>` (optional, for grouping)

## Test Structure

### Arrange-Act-Assert Pattern
Always structure tests with clear AAA sections:

```python
def test_create_airline_with_valid_data_returns_airline():
    # Arrange
    repository = InMemoryAirlineRepository()
    id_generator = FixedIdGenerator("test-id")
    use_case = CreateAirlineUseCase(repository, id_generator)
    request = CreateAirlineDTO(name="Delta", country="US")
    
    # Act
    result = use_case.execute(request)
    
    # Assert
    assert result.id == "test-id"
    assert result.name == "Delta"
    assert result.country == "US"
```

### Test Naming
Use descriptive names that explain what is being tested:

```python
# Good
def test_rename_airline_with_valid_name_returns_new_instance():
    pass

def test_rename_airline_with_empty_name_raises_validation_error():
    pass

# Bad
def test_rename():
    pass

def test_airline():
    pass
```

## Unit Testing

### Domain Layer Tests
- Test business logic in isolation
- Test immutability of entities
- Test validation rules
- No external dependencies or mocks needed

```python
def test_airline_rename_returns_new_instance():
    # Test immutability
    airline = Airline(id="1", name="Old Name", country="US")
    renamed = airline.rename("New Name")
    
    assert renamed.name == "New Name"
    assert airline.name == "Old Name"
    assert renamed is not airline
```

### Application Layer Tests
- Use in-memory implementations instead of mocks
- Test use case orchestration
- Test error handling and edge cases

```python
def test_create_airline_saves_to_repository():
    # Arrange
    repository = InMemoryAirlineRepository()
    id_generator = FixedIdGenerator("test-id")
    use_case = CreateAirlineUseCase(repository, id_generator)
    request = CreateAirlineDTO(name="Delta", country="US")
    
    # Act
    result = use_case.execute(request)
    
    # Assert
    saved_airline = repository.find_by_id("test-id")
    assert saved_airline is not None
    assert saved_airline.name == "Delta"
```

## Integration Testing

### API Tests
Use FastAPI's TestClient for API integration tests:

```python
from fastapi.testclient import TestClient

def test_create_airline_endpoint():
    client = TestClient(app)
    
    response = client.post(
        "/airlines",
        json={"name": "Delta Airlines", "country": "US"}
    )
    
    assert response.status_code == 201
    assert response.json()["name"] == "Delta Airlines"
```

### Infrastructure Tests
Test repository implementations with real or test databases:

```python
def test_sql_repository_saves_and_retrieves_airline(db_session):
    repository = SqlAirlineRepository(db_session)
    airline = Airline(id="1", name="Delta", country="US")
    
    repository.save(airline)
    retrieved = repository.find_by_id("1")
    
    assert retrieved == airline
```

## Fixtures

### Pytest Fixtures
Define reusable fixtures in `conftest.py` or test modules:

```python
# conftest.py
import pytest

@pytest.fixture
def airline_repository():
    return InMemoryAirlineRepository()

@pytest.fixture
def fixed_id_generator():
    return FixedIdGenerator("test-id")

@pytest.fixture
def sample_airline():
    return Airline(id="1", name="Delta", country="US")
```

### Factory Functions
Create factory functions for test data:

```python
# tests/fixtures/factories.py
def create_airline(
    id: str = "test-id",
    name: str = "Test Airline",
    country: str = "US"
) -> Airline:
    return Airline(id=id, name=name, country=country)
```

## Mocking and Fakes

### Prefer In-Memory Implementations
Instead of mocking, create in-memory implementations:

```python
# tests/fixtures/in_memory_repository.py
class InMemoryAirlineRepository:
    def __init__(self):
        self._airlines: dict[str, Airline] = {}
    
    def find_by_id(self, airline_id: str) -> Airline | None:
        return self._airlines.get(airline_id)
    
    def save(self, airline: Airline) -> None:
        self._airlines[airline.id] = airline
```

### When to Use Mocks
Only mock external dependencies that are difficult to simulate:
- External APIs
- Payment gateways
- Email services

```python
from unittest.mock import Mock

def test_send_notification_calls_email_service():
    email_service = Mock()
    use_case = NotifyUserUseCase(email_service)
    
    use_case.execute("user@example.com", "Hello")
    
    email_service.send.assert_called_once_with("user@example.com", "Hello")
```

## Test Coverage

### Coverage Goals
- Domain layer: 95%+ coverage
- Application layer: 90%+ coverage
- Infrastructure layer: 80%+ coverage
- API layer: 85%+ coverage

### Running Coverage
```bash
pytest --cov=. --cov-report=html --cov-report=term
```

## Parametrized Tests

Use `pytest.mark.parametrize` for testing multiple scenarios:

```python
import pytest

@pytest.mark.parametrize("name,expected_valid", [
    ("Delta Airlines", True),
    ("", False),
    ("A" * 101, False),
])
def test_airline_name_validation(name, expected_valid):
    if expected_valid:
        airline = Airline(id="1", name=name, country="US")
        assert airline.name == name
    else:
        with pytest.raises(ValidationError):
            Airline(id="1", name=name, country="US")
```

## Async Testing

### Testing Async Functions
```python
import pytest

@pytest.mark.asyncio
async def test_async_use_case():
    use_case = AsyncUseCase()
    result = await use_case.execute()
    assert result is not None
```

## Test Data Management

### Test Database Setup
```python
@pytest.fixture(scope="function")
def db_session():
    # Setup test database
    engine = create_test_engine()
    Base.metadata.create_all(engine)
    session = Session(engine)
    
    yield session
    
    # Teardown
    session.close()
    Base.metadata.drop_all(engine)
```

## Best Practices

### Keep Tests Independent
- Each test should be able to run in isolation
- Don't rely on test execution order
- Clean up state after each test

### One Assertion Per Test (Guideline)
- Prefer one logical assertion per test
- Related assertions are acceptable (e.g., checking object state)

### Test Edge Cases
- Null/None values
- Empty collections
- Boundary values
- Invalid inputs

### Don't Test Implementation Details
- Test behavior, not internal implementation
- Tests should not break when refactoring internal logic

### Keep Tests Simple
- Tests should be easier to understand than the code they test
- Avoid complex logic in tests
- Don't reuse production code in tests
