# Agent Prompt: Generate Test Coverage

**Purpose:** Generate comprehensive tests for new or existing features following Clean Architecture patterns.

**When to use:** After implementing a new endpoint, use case, or entity.

---

## Quick Start

1. Copy the prompt template below
2. Replace `[PLACEHOLDERS]` with your specifics
3. Paste into Copilot Chat with `@workspace`
4. Review and refine generated tests
5. Run tests to validate

---

## Prompt Template

```
@workspace Generate comprehensive tests for [ENTITY_NAME] [FEATURE].

Context:
- Service: [SERVICE_NAME] (e.g., airline-catalog)
- Files changed: [LIST_FILES]
- Test type: [unit | integration | both]

Requirements:
- Follow existing test patterns in tests/unit/ and tests/integration/
- Use pytest fixtures from existing tests (see test_use_cases.py for repository fixture pattern)
- Test happy path and edge cases
- Include error scenarios (404, 400, 422, 409)
- Ensure test isolation (fresh repository instance per test)
- Use FastAPI TestClient for integration tests
- Add descriptive docstrings explaining what each test validates
- Follow naming convention: test_[action]_[scenario]

Specific test cases needed:
1. [Describe specific scenario to test]
2. [Describe error scenario]
3. [Describe edge case]
4. [Add more as needed]

Generate tests that achieve 90%+ coverage of the new code.
Follow the Clean Architecture layers:
- Domain tests: Validate entity business rules
- Application tests: Validate use case logic with mocked repositories
- Integration tests: Validate API endpoints end-to-end
```

---

## Example Usage

### Example 1: Generate Tests for Existing Feature

```
@workspace Generate comprehensive tests for Airline CRUD operations.

Context:
- Service: airline-catalog
- Files changed: api/routes.py, application/use_cases.py, domain/models.py
- Test type: both unit and integration

Requirements:
- Follow existing test patterns in tests/unit/ and tests/integration/
- Use pytest fixtures from existing tests (see test_use_cases.py for repository fixture pattern)
- Test happy path and edge cases
- Include error scenarios (404, 400, 422, 409)
- Ensure test isolation (fresh repository instance per test)
- Use FastAPI TestClient for integration tests
- Add descriptive docstrings explaining what each test validates
- Follow naming convention: test_[action]_[scenario]

Specific test cases needed:
1. Create airline with invalid IATA code (not exactly 2 characters)
2. Create airline with empty name or country
3. Create airline with duplicate code (409 conflict)
4. Update non-existent airline returns 404
5. Update airline with partial data (only name, only country)
6. List airlines with active_only=true filter
7. Delete airline that doesn't exist returns 404
8. Get airline by non-existent ID returns 404

Generate tests that achieve 90%+ coverage of the new code.
Follow the Clean Architecture layers:
- Domain tests: Validate entity business rules (Airline validation)
- Application tests: Validate use case logic with InMemoryAirlineRepository
- Integration tests: Validate API endpoints end-to-end with TestClient
```

### Example 2: Generate Tests for New Entity

```
@workspace Generate comprehensive tests for the new Airport entity.

Context:
- Service: airline-catalog
- Files changed: domain/models.py (Airport class), domain/interfaces.py (AirportRepository), application/use_cases.py (Airport use cases), api/routes.py (Airport endpoints)
- Test type: both unit and integration

Requirements:
- Follow existing test patterns from Airline tests
- Use pytest fixtures from existing tests
- Test happy path and edge cases
- Include error scenarios (404, 400, 422, 409)
- Ensure test isolation (fresh repository instance per test)
- Use FastAPI TestClient for integration tests
- Add descriptive docstrings explaining what each test validates
- Follow naming convention: test_[action]_[scenario]

Specific test cases needed:
1. Create airport with valid IATA code (3 characters)
2. Create airport with invalid IATA code (not 3 chars)
3. Create airport with duplicate code
4. Validate airport code is uppercase
5. Search airports by city
6. List airports by country
7. Update airport timezone
8. Deactivate/activate airport

Generate tests that achieve 90%+ coverage of the new code.
Follow the Clean Architecture layers:
- Domain tests: Validate Airport entity business rules
- Application tests: Validate Airport use cases with mock repository
- Integration tests: Validate Airport API endpoints end-to-end
```

---

## After Generation

### 1. Run Tests
```bash
# Run all generated tests
pytest tests/ -v

# Run specific test file
pytest tests/unit/test_domain_models.py -v

# Run with coverage
pytest --cov=domain --cov=application --cov=api --cov-report=html
```

### 2. Review Coverage Report
```bash
# Open coverage report in browser
open htmlcov/index.html

# Check coverage percentage
pytest --cov=. --cov-report=term-missing
```

### 3. Identify Gaps
- Look for uncovered lines in htmlcov/
- Check edge cases not covered
- Verify error handling paths tested

### 4. Iterate If Needed
```
@workspace Add tests for the following uncovered scenarios:
- [Scenario from coverage report]
- [Edge case discovered]
- [Error path not tested]
```

### 5. Validate & Commit
```bash
# Ensure all tests pass
pytest tests/

# Check code quality
ruff check .

# Commit tests with feature
git add tests/ domain/ application/ api/
git commit -m "Add Airport entity with comprehensive tests"
```

---

## Best Practices

### ✅ Do This

- **Be specific** in your prompt about edge cases
- **Reference existing tests** for pattern consistency
- **Run tests incrementally** as they're generated
- **Review generated code** - agents can make mistakes
- **Use coverage reports** to identify gaps
- **Test business rules** in domain layer
- **Test use case logic** with mocked dependencies
- **Test API contracts** end-to-end

### ❌ Avoid This

- **Blindly accepting** generated tests without review
- **Skipping coverage checks** - always verify
- **Testing implementation details** - test behavior
- **Coupling tests** - each test should be independent
- **Ignoring test failures** - fix or remove bad tests
- **Over-mocking** - use real dependencies when simple (like in-memory repo)

---

## Coverage Targets

| Layer | Target Coverage | Priority |
|-------|----------------|----------|
| Domain | 100% | Critical - core business logic |
| Application | 90%+ | High - use case orchestration |
| API | 85%+ | High - contract validation |
| Infrastructure | 70%+ | Medium - adapter logic |

---

## Test Structure Reference

### Domain Layer Tests
```python
def test_entity_creation():
    """Test creating a valid entity."""
    # Arrange
    # Act
    # Assert

def test_entity_validation():
    """Test entity business rules."""
    with pytest.raises(ValueError):
        # Invalid entity creation
```

### Application Layer Tests
```python
@pytest.fixture
def repository():
    """Provide a fresh repository for each test."""
    return InMemoryRepository()

def test_use_case_success(repository):
    """Test successful use case execution."""
    use_case = CreateEntityUseCase(repository)
    # Test logic
```

### Integration Tests
```python
@pytest.fixture
def client():
    """Create test client with fresh dependencies."""
    # Setup
    yield test_client
    # Teardown

def test_api_endpoint(client):
    """Test API endpoint end-to-end."""
    response = client.post("/api/v1/entities/", json={...})
    assert response.status_code == 201
```

---

## Troubleshooting

**Problem:** Agent generates tests that don't follow project patterns
**Solution:** Reference specific test files in prompt: "Follow the pattern in tests/integration/test_api.py"

**Problem:** Tests have import errors
**Solution:** Ensure PYTHONPATH is set: `export PYTHONPATH=$PWD`

**Problem:** Tests are too slow
**Solution:** Use in-memory repositories for unit tests, avoid database calls

**Problem:** Coverage is still low after generation
**Solution:** Ask agent specifically for uncovered lines: "Generate tests for lines 45-67 in use_cases.py"

---

## Related Prompts

- `agent-add-entity.md` - Generate new domain entities with tests
- `agent-add-repository.md` - Generate database repository implementations with tests
- `agent-refactor-code.md` - Refactor code while maintaining test coverage
