# Infrastructure Layer Instructions

Files in the `infrastructure/` directory provide concrete implementations of domain interfaces.

## Repository Implementations

- Implement domain Protocol interfaces
- Handle data persistence concerns (SQL, NoSQL, file system)
- Support multiple implementations (e.g., SqlRepository, InMemoryRepository)

```python
class SqlUserRepository:
    """SQL implementation of UserRepository protocol."""
    
    def __init__(self, session: Session):
        self._session = session
    
    def find_by_id(self, user_id: str) -> User | None:
        db_user = self._session.query(UserModel).filter_by(id=user_id).first()
        return self._to_domain(db_user) if db_user else None
```

## Database Concerns

- Database models belong in `infrastructure/database/`
- Separate database models from domain entities
- Implement mapping functions: `_to_domain()` and `_from_domain()`
- Handle transactions at the infrastructure boundary

## External Services

- Implement external API clients in `infrastructure/services/`
- Handle HTTP calls, authentication, retries
- Transform external data to domain models
- Isolate third-party SDK usage

## Testing Implementations

- Provide InMemory implementations for testing
- InMemory implementations should match production behavior
- Store data in dictionaries or lists for test speed

```python
class InMemoryUserRepository:
    """In-memory implementation for testing."""
    
    def __init__(self):
        self._users: dict[str, User] = {}
    
    def find_by_id(self, user_id: str) -> User | None:
        return self._users.get(user_id)
```

## What to Include

- ✓ ORM models and database schemas
- ✓ API clients and external service wrappers
- ✓ File system operations
- ✓ Caching implementations
- ✓ Message queue producers/consumers
