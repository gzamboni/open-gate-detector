# Use an official Python runtime as a parent image
# This base image supports both x86_64 and arm64 architectures
FROM --platform=$TARGETPLATFORM python:3.11-slim

# Add build argument for platform targeting
ARG TARGETPLATFORM

# Set the working directory in the container
WORKDIR /app

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    API_TOKEN=default-secure-token

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    gcc \
    g++ \
    libgl1 \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Print platform information for debugging
RUN echo "Building for platform: $TARGETPLATFORM"

# Copy requirements file
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the project code
COPY . .

# Expose the port the app runs on
EXPOSE 8000

# Command to run the application
CMD ["python", "run.py"]
