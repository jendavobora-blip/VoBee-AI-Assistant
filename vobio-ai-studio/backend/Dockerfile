FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements_full.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements_full.txt

# Copy application code
COPY . .

# Create necessary directories
RUN mkdir -p /app/quarantine /app/logs /app/temp /app/skills /app/knowledge

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
  CMD curl -f http://localhost:8000/health || exit 1

# Run the application
CMD ["python", "api_server_integrated.py"]
