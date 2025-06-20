# Use an official Python image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y build-essential curl && rm -rf /var/lib/apt/lists/*

# Copy requirements and install them
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the whole app directory
COPY . ./agent

# Expose FastAPI port
EXPOSE 8000

# Start FastAPI with Uvicorn using module path
CMD ["uvicorn", "agent.main:app", "--host", "0.0.0.0", "--port", "8000"]
