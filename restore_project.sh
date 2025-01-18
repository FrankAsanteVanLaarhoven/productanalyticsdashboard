#!/bin/bash

# Stop any running containers
docker-compose down

# Start the containers
docker-compose up -d

# Wait for services to be ready
echo "Waiting for services to start..."
sleep 10

# Verify services
docker-compose ps

# Show DAGs status
docker-compose exec webserver airflow dags list

echo "Project restored!"
