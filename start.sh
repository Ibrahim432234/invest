#!/bin/bash

# Pull latest changes
git pull

# Clean up any previous Docker builds
docker-compose down -v
docker system prune -f

# Rebuild and start
docker-compose up --build -d

# Show logs
docker-compose logs -f
