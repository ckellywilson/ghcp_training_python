# Airline Service

Microservice for managing airline operations following Clean Architecture principles.

## Architecture

This service follows Clean Architecture with strict layer boundaries:
- **Domain**: Pure business logic and entities
- **Application**: Use cases and DTOs
- **Infrastructure**: External dependencies and data access
- **API**: FastAPI routes and dependency injection

## Running Locally

```bash
# Install dependencies
pip install -r requirements.txt

# Run the service
uvicorn main:app --reload --port 8001

# Run tests
pytest tests/
```

## Docker

```bash
# Build image
docker build -t airline-service .

# Run container
docker run -p 8001:8000 airline-service
```

## API Endpoints

- `GET /airlines` - List all airlines
- `POST /airlines` - Create new airline
- `GET /airlines/{id}` - Get airline by ID
- `PUT /airlines/{id}` - Update airline
- `DELETE /airlines/{id}` - Delete airline
- `GET /health` - Health check endpoint

## Environment Variables

- `LOG_LEVEL`: Logging level (default: INFO)
- `DATABASE_URL`: Database connection string (when using persistent storage)
