.PHONY: help build up down restart logs clean shell test

# Default target
help:
	@echo "🧠 AI Code Auditor - Docker Commands"
	@echo "====================================="
	@echo ""
	@echo "Available commands:"
	@echo "  make build     - Build the Docker image"
	@echo "  make up        - Start the application"
	@echo "  make down      - Stop the application"
	@echo "  make restart   - Restart the application"
	@echo "  make logs      - View application logs"
	@echo "  make shell     - Open a shell in the container"
	@echo "  make clean     - Remove containers, images, and volumes"
	@echo "  make test      - Run tests in container"
	@echo "  make rebuild   - Rebuild and restart"
	@echo ""
	@echo "Quick start: make build && make up"
	@echo "Access at: http://localhost:8501"

# Build the Docker image
build:
	@echo "🏗️  Building Docker image..."
	docker-compose build

# Start the application
up:
	@echo "🚀 Starting AI Code Auditor..."
	docker-compose up -d
	@echo ""
	@echo "✅ AI Code Auditor is running!"
	@echo "📍 Access it at: http://localhost:8501"
	@echo ""
	@echo "💡 View logs with: make logs"

# Stop the application
down:
	@echo "🛑 Stopping AI Code Auditor..."
	docker-compose down
	@echo "✅ Stopped"

# Restart the application
restart: down up

# Rebuild and restart
rebuild:
	@echo "🔄 Rebuilding application..."
	docker-compose down
	docker-compose build --no-cache
	docker-compose up -d
	@echo "✅ Rebuild complete!"

# View logs
logs:
	@echo "📋 Viewing logs (Press Ctrl+C to exit)..."
	docker-compose logs -f

# Open shell in container
shell:
	@echo "🐚 Opening shell in container..."
	docker-compose exec ai-code-auditor /bin/bash

# Clean up everything
clean:
	@echo "🧹 Cleaning up containers, images, and volumes..."
	docker-compose down -v
	docker rmi ai-code-auditor-ai-code-auditor 2>/dev/null || true
	@echo "✅ Cleanup complete"

# Run tests (if you add tests later)
test:
	@echo "🧪 Running tests..."
	docker-compose exec ai-code-auditor pytest tests/ -v

# Check container status
status:
	@echo "📊 Container Status:"
	@docker-compose ps

# Show container stats
stats:
	@echo "📈 Container Stats:"
	@docker stats ai-code-auditor --no-stream