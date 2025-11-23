# 🐳 Docker Deployment Guide

Complete guide for deploying AI Code Auditor using Docker.

## 📋 Prerequisites

- **Docker** (version 20.10 or higher)
- **Docker Compose** (version 2.0 or higher)
- **OpenAI API Key** (get from [platform.openai.com](https://platform.openai.com/api-keys))

### Installing Docker

#### Linux (Ubuntu/Debian)
```bash
# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Install Docker Compose
sudo apt-get update
sudo apt-get install docker-compose-plugin

# Add your user to docker group
sudo usermod -aG docker $USER
```

#### macOS
```bash
# Using Homebrew
brew install --cask docker

# Or download Docker Desktop from:
# https://www.docker.com/products/docker-desktop
```

#### Windows
Download and install Docker Desktop from:
https://www.docker.com/products/docker-desktop

---

## 🚀 Quick Start (3 Easy Steps)

### 1. Clone and Configure
```bash
git clone https://github.com/Fustli/ai-code-auditor.git
cd ai-code-auditor

# Copy environment template
cp .env.example .env

# Edit .env and add your OpenAI API key
nano .env  # or use any text editor
```

### 2. Build and Run
```bash
# Using the interactive script
./docker-start.sh

# OR using Docker Compose directly
docker-compose up -d

# OR using Make
make build && make up
```

### 3. Access the Application
Open your browser to: **http://localhost:8501**

---

## 📖 Detailed Usage

### Using the Interactive Script (Recommended)

The `docker-start.sh` script provides a user-friendly menu:

```bash
./docker-start.sh
```

Options:
1. **Build and start** - First time setup
2. **Start** - Start existing container
3. **Stop** - Stop the application
4. **Rebuild** - Rebuild from scratch
5. **View logs** - Monitor application logs
6. **Clean up** - Remove everything

### Using Docker Compose

#### Basic Commands
```bash
# Build the image
docker-compose build

# Start in detached mode
docker-compose up -d

# Start with logs visible
docker-compose up

# Stop the application
docker-compose down

# Stop and remove volumes
docker-compose down -v

# View logs
docker-compose logs -f

# Restart
docker-compose restart
```

### Using Makefile (Advanced)

```bash
# View all available commands
make help

# Build the image
make build

# Start the application
make up

# View logs
make logs

# Stop the application
make down

# Restart
make restart

# Rebuild from scratch
make rebuild

# Open shell in container
make shell

# Clean up everything
make clean

# Check container status
make status
```

---

## ⚙️ Configuration

### Environment Variables

Edit the `.env` file:

```bash
# Required
OPENAI_API_KEY=sk-your-api-key-here

# Optional
OPENAI_MODEL=gpt-4o              # AI model to use
MAX_TOKENS=4000                  # Max response tokens
TEMPERATURE=0.1                  # Response creativity (0-1)
```

### Custom Port

To use a different port, edit `docker-compose.yml`:

```yaml
ports:
  - "8080:8501"  # Change 8080 to your desired port
```

### Resource Limits

Add resource limits in `docker-compose.yml`:

```yaml
services:
  ai-code-auditor:
    # ... existing config ...
    deploy:
      resources:
        limits:
          cpus: '2'
          memory: 2G
        reservations:
          memory: 512M
```

---

## 🔧 Development Setup

### Hot Reload (Development Mode)

The default `docker-compose.yml` includes volume mounts for development:

```yaml
volumes:
  - ./src:/app/src
  - ./examples:/app/examples
```

This allows you to edit code locally and see changes immediately.

### Running with Custom Code

```bash
# Mount your code directory
docker run -d \
  -p 8501:8501 \
  -v $(pwd)/my-code:/app/custom-code \
  -e OPENAI_API_KEY=your-key \
  ai-code-auditor
```

---

## 📊 Monitoring

### View Logs
```bash
# Follow logs
docker-compose logs -f

# Last 100 lines
docker-compose logs --tail=100

# Specific service logs
docker-compose logs -f ai-code-auditor
```

### Check Container Status
```bash
# Container status
docker-compose ps

# Resource usage
docker stats ai-code-auditor

# Container details
docker inspect ai-code-auditor
```

### Health Check
```bash
# Check health status
docker-compose ps

# Manual health check
curl http://localhost:8501/_stcore/health
```

---

## 🐛 Troubleshooting

### Container Won't Start

**Problem:** Container fails to start

**Solution:**
```bash
# Check logs for errors
docker-compose logs

# Rebuild without cache
docker-compose build --no-cache

# Remove old containers and volumes
docker-compose down -v
```

### API Key Issues

**Problem:** API key not recognized

**Solution:**
```bash
# Verify .env file exists
cat .env

# Ensure API key is set correctly
grep OPENAI_API_KEY .env

# Restart container to reload environment
docker-compose restart
```

### Port Already in Use

**Problem:** Port 8501 is already taken

**Solution:**
```bash
# Find process using port
sudo lsof -i :8501

# Change port in docker-compose.yml
# Edit: ports: - "8502:8501"
```

### Permission Issues

**Problem:** Permission denied errors

**Solution:**
```bash
# On Linux, add user to docker group
sudo usermod -aG docker $USER
newgrp docker

# Or run with sudo (not recommended)
sudo docker-compose up -d
```

### Out of Memory

**Problem:** Container crashes due to memory

**Solution:**
Add memory limits in `docker-compose.yml`:
```yaml
mem_limit: 2g
mem_reservation: 512m
```

---

## 🔐 Security Best Practices

### 1. API Key Management
```bash
# Never commit .env to git
echo ".env" >> .gitignore

# Use Docker secrets (production)
docker secret create openai_key .env
```

### 2. Network Security
```bash
# Use custom network
networks:
  ai-code-auditor:
    driver: bridge
    internal: true  # No external access
```

### 3. Read-Only Filesystem
```yaml
services:
  ai-code-auditor:
    read_only: true
    tmpfs:
      - /tmp
      - /app/.streamlit
```

---

## 🚢 Production Deployment

### Docker Swarm

```bash
# Initialize swarm
docker swarm init

# Deploy stack
docker stack deploy -c docker-compose.yml ai-code-auditor

# Scale service
docker service scale ai-code-auditor_app=3
```

### Kubernetes

Create a `kubernetes.yaml`:
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: ai-code-auditor
spec:
  replicas: 2
  selector:
    matchLabels:
      app: ai-code-auditor
  template:
    metadata:
      labels:
        app: ai-code-auditor
    spec:
      containers:
      - name: ai-code-auditor
        image: ai-code-auditor:latest
        ports:
        - containerPort: 8501
        env:
        - name: OPENAI_API_KEY
          valueFrom:
            secretKeyRef:
              name: openai-secret
              key: api-key
```

### Behind Nginx Reverse Proxy

```nginx
server {
    listen 80;
    server_name code-auditor.example.com;

    location / {
        proxy_pass http://localhost:8501;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

---

## 📦 Building Custom Images

### Custom Dockerfile

```dockerfile
FROM ai-code-auditor:latest

# Add custom dependencies
RUN pip install your-package

# Add custom configuration
COPY custom-config.py /app/

# Override entrypoint
CMD ["streamlit", "run", "app.py", "--server.port=8501"]
```

### Multi-Stage Build

```dockerfile
# Builder stage
FROM python:3.11-slim as builder
WORKDIR /app
COPY requirements.txt .
RUN pip install --user -r requirements.txt

# Runtime stage
FROM python:3.11-slim
WORKDIR /app
COPY --from=builder /root/.local /root/.local
COPY . .
CMD ["streamlit", "run", "app.py"]
```

---

## 🔄 Updates and Maintenance

### Updating the Application

```bash
# Pull latest code
git pull origin main

# Rebuild and restart
docker-compose down
docker-compose build --no-cache
docker-compose up -d
```

### Backup and Restore

```bash
# Backup volumes
docker run --rm -v ai-code-auditor-data:/data \
  -v $(pwd):/backup alpine \
  tar czf /backup/backup.tar.gz -C /data .

# Restore volumes
docker run --rm -v ai-code-auditor-data:/data \
  -v $(pwd):/backup alpine \
  tar xzf /backup/backup.tar.gz -C /data
```

---

## 📚 Additional Resources

- **Docker Documentation:** https://docs.docker.com/
- **Docker Compose Docs:** https://docs.docker.com/compose/
- **Streamlit in Docker:** https://docs.streamlit.io/knowledge-base/tutorials/deploy/docker
- **OpenAI API Docs:** https://platform.openai.com/docs

---

## 💡 Tips and Tricks

### 1. Faster Builds
```bash
# Use BuildKit for faster builds
DOCKER_BUILDKIT=1 docker-compose build
```

### 2. Reduce Image Size
```bash
# Multi-stage builds
# Use slim base images
# Clean up in same RUN command
RUN apt-get update && apt-get install -y package \
    && apt-get clean && rm -rf /var/lib/apt/lists/*
```

### 3. Development Workflow
```bash
# Start with logs
docker-compose up

# In another terminal, make changes
# Streamlit will auto-reload
```

### 4. Debugging
```bash
# Access container shell
docker-compose exec ai-code-auditor /bin/bash

# Run commands inside container
docker-compose exec ai-code-auditor python -c "import openai; print(openai.__version__)"
```

---

## ❓ FAQ

**Q: Do I need to install Python?**
A: No! Docker includes everything you need.

**Q: Can I use this on Windows?**
A: Yes! Install Docker Desktop for Windows.

**Q: How much disk space is needed?**
A: Approximately 1-2 GB for the Docker image.

**Q: Can I run multiple instances?**
A: Yes, just change the port mapping.

**Q: Is GPU support available?**
A: The AI runs via OpenAI API, so no GPU needed locally.

---

For more information, visit the [main README](README.md) or [open an issue](https://github.com/Fustli/ai-code-auditor/issues).