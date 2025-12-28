#!/bin/bash
# Run tests for all microservices

set -e

echo "Running tests for all microservices..."

# Test airline service
echo "Testing airline-service..."
cd services/airline-service
python -m pytest tests/ -v --cov=. --cov-report=term
cd ../..

echo "✅ All tests passed"
