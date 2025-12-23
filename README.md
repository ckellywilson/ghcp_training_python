# Airline Catalog Microservice

A FastAPI microservice for managing airline catalog data, built following Clean Architecture principles.

## Architecture

This project follows Clean Architecture with strict separation of concerns:

- **Domain Layer**: Pure business logic with `Airline` entity and `AirlineRepository` protocol
- **Application Layer**: Use cases and DTOs (Pydantic models) for airline operations
- **Infrastructure Layer**: Concrete implementations (currently in-memory repository)
- **API Layer**: FastAPI routes and dependency injection configuration

## Dependencies

Dependencies flow inward:
- API → Application → Domain
- Infrastructure implements Domain interfaces
- No framework dependencies in Domain or Application layers

## Getting Started

### Installation

```bash
# Install dependencies
pip install -r requirements.txt
```

### Running the Application

```bash
# Run with uvicorn
uvicorn main:app --reload

# Or run directly
python main.py
```

The API will be available at `http://localhost:8000`

### API Documentation

- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## API Endpoints

### Airlines

- `POST /api/v1/airlines/` - Create a new airline
- `GET /api/v1/airlines/` - List all airlines (optional query param: `active_only=true`)
- `GET /api/v1/airlines/{airline_id}` - Get airline by ID
- `PUT /api/v1/airlines/{airline_id}` - Update airline
- `DELETE /api/v1/airlines/{airline_id}` - Delete airline

### Health Check

- `GET /health` - Service health status

## Example Usage

### Create an Airline

```bash
curl -X POST "http://localhost:8000/api/v1/airlines/" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "American Airlines",
    "code": "AA",
    "country": "United States",
    "active": true
  }'
```

### List All Airlines

```bash
curl "http://localhost:8000/api/v1/airlines/"
```

### List Active Airlines Only

```bash
curl "http://localhost:8000/api/v1/airlines/?active_only=true"
```

## Testing

```bash
# Run tests
pytest

# Run with coverage
pytest --cov=. --cov-report=html
```

## Project Structure

```
.
├── domain/
│   ├── models.py          # Airline entity
│   └── interfaces.py      # AirlineRepository protocol
├── application/
│   ├── dtos.py           # Pydantic DTOs
│   └── use_cases.py      # Business use cases
├── infrastructure/
│   └── repositories/
│       └── in_memory_airline_repository.py
├── api/
│   ├── routes.py         # FastAPI endpoints
│   └── di.py            # Dependency injection
├── tests/
│   ├── unit/
│   ├── integration/
│   └── fixtures/
├── main.py              # Application entry point
└── requirements.txt     # Python dependencies
```

## Development Guidelines

- Use Python 3.11+
- Follow PEP 8 style guide
- Use `Protocol` for interface definitions (not ABC)
- Keep domain and application layers framework-agnostic
- Write tests for all business logic
- Use type hints throughout

## Future Enhancements

- Add database persistence (PostgreSQL/MongoDB)
- Implement authentication and authorization
- Add caching layer
- Add API rate limiting
- Add logging and monitoring
- Add CI/CD pipeline
