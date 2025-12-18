FROM python:3.11-slim

WORKDIR /app

# Install Docker CLI for Docker-in-Docker
RUN apt-get update && apt-get install -y \
    docker.io \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY *.py ./

# Expose port
EXPOSE 5040

# Run the application
CMD ["python", "main.py"]
