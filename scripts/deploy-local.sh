#!/bin/bash
# Deploy all services locally using Docker Compose

set -e

echo "Starting local deployment..."

# Start all services
docker-compose up -d

echo "Waiting for services to be healthy..."
sleep 10

# Check health of services
echo "Checking service health..."
curl -f http://localhost:8001/health || echo "⚠️ Airline service not responding"

echo "✅ Local deployment complete"
echo ""
echo "Services running at:"
echo "  - Airline Service: http://localhost:8001"
echo "  - PostgreSQL: localhost:5432"
echo "  - Redis: localhost:6379"
echo "  - Azurite: localhost:10000-10002"
echo ""
echo "To view logs: docker-compose logs -f"
echo "To stop: docker-compose down"
