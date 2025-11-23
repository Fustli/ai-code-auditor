#!/bin/bash

# AI Code Auditor - Docker Quick Start Script
# This script helps you set up and run the AI Code Auditor using Docker

set -e

echo "🧠 AI Code Auditor - Docker Setup"
echo "=================================="
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo -e "${RED}❌ Docker is not installed.${NC}"
    echo "Please install Docker from: https://docs.docker.com/get-docker/"
    exit 1
fi

echo -e "${GREEN}✅ Docker is installed${NC}"

# Check if Docker Compose is installed
if ! command -v docker-compose &> /dev/null && ! docker compose version &> /dev/null; then
    echo -e "${RED}❌ Docker Compose is not installed.${NC}"
    echo "Please install Docker Compose from: https://docs.docker.com/compose/install/"
    exit 1
fi

echo -e "${GREEN}✅ Docker Compose is installed${NC}"
echo ""

# Check for .env file
if [ ! -f .env ]; then
    echo -e "${YELLOW}⚠️  No .env file found.${NC}"
    echo "Creating .env file from template..."
    
    if [ -f .env.example ]; then
        cp .env.example .env
        echo -e "${GREEN}✅ Created .env file${NC}"
        echo ""
        echo -e "${YELLOW}⚠️  IMPORTANT: Please edit the .env file and add your OpenAI API key!${NC}"
        echo "   Get your API key from: https://platform.openai.com/api-keys"
        echo ""
        read -p "Press Enter to continue after adding your API key..."
    else
        echo -e "${RED}❌ .env.example not found${NC}"
        exit 1
    fi
else
    echo -e "${GREEN}✅ .env file exists${NC}"
fi

echo ""
echo "Choose an option:"
echo "1) Build and start the application"
echo "2) Start the application (if already built)"
echo "3) Stop the application"
echo "4) Rebuild the application"
echo "5) View logs"
echo "6) Clean up (remove containers and images)"
echo ""
read -p "Enter your choice (1-6): " choice

case $choice in
    1)
        echo ""
        echo -e "${BLUE}🏗️  Building Docker image...${NC}"
        docker-compose build
        
        echo ""
        echo -e "${BLUE}🚀 Starting AI Code Auditor...${NC}"
        docker-compose up -d
        
        echo ""
        echo -e "${GREEN}✅ AI Code Auditor is starting!${NC}"
        echo ""
        echo "📍 The application will be available at: http://localhost:8501"
        echo "⏱️  Please wait 10-15 seconds for the application to fully start"
        echo ""
        echo "To view logs, run: docker-compose logs -f"
        echo "To stop, run: docker-compose down"
        ;;
        
    2)
        echo ""
        echo -e "${BLUE}🚀 Starting AI Code Auditor...${NC}"
        docker-compose up -d
        
        echo ""
        echo -e "${GREEN}✅ AI Code Auditor is running!${NC}"
        echo "📍 Access it at: http://localhost:8501"
        ;;
        
    3)
        echo ""
        echo -e "${BLUE}🛑 Stopping AI Code Auditor...${NC}"
        docker-compose down
        
        echo ""
        echo -e "${GREEN}✅ AI Code Auditor stopped${NC}"
        ;;
        
    4)
        echo ""
        echo -e "${BLUE}🔄 Rebuilding AI Code Auditor...${NC}"
        docker-compose down
        docker-compose build --no-cache
        docker-compose up -d
        
        echo ""
        echo -e "${GREEN}✅ AI Code Auditor rebuilt and started!${NC}"
        echo "📍 Access it at: http://localhost:8501"
        ;;
        
    5)
        echo ""
        echo -e "${BLUE}📋 Viewing logs (Press Ctrl+C to exit)...${NC}"
        echo ""
        docker-compose logs -f
        ;;
        
    6)
        echo ""
        echo -e "${YELLOW}⚠️  This will remove all containers, images, and volumes.${NC}"
        read -p "Are you sure? (y/N): " confirm
        
        if [ "$confirm" = "y" ] || [ "$confirm" = "Y" ]; then
            echo ""
            echo -e "${BLUE}🧹 Cleaning up...${NC}"
            docker-compose down -v
            docker rmi ai-code-auditor-ai-code-auditor 2>/dev/null || true
            
            echo ""
            echo -e "${GREEN}✅ Cleanup complete${NC}"
        else
            echo "Cancelled."
        fi
        ;;
        
    *)
        echo -e "${RED}❌ Invalid choice${NC}"
        exit 1
        ;;
esac