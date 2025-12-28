#!/bin/bash
# Build all microservices

set -e

echo "Building all microservices..."

# Build airline service
echo "Building airline-service..."
docker build -t airline-service:latest ./services/airline-service

echo "✅ All services built successfully"
