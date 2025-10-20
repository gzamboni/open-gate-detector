# Open Gate Detector

A computer vision-based API service that detects whether a gate is open or closed using RTSP camera feeds.

## Overview

The Open Gate Detector is a FastAPI-based service that connects to IP cameras via RTSP, captures frames, and uses computer vision techniques to determine if a gate is open or closed. This can be integrated with home automation systems or security applications to monitor gate status.

## Features

- **Gate Status Detection**: Uses Hough Line Transform to detect vertical lines in camera images to determine if a gate is open or closed
- **RESTful API**: Provides a simple API endpoint to check gate status
- **Authentication**: Secures API access with Bearer token authentication
- **Kubernetes Ready**: Includes Kubernetes manifests for deployment with ArgoCD
- **Docker Support**: Containerized for easy deployment

## How It Works

1. The service connects to an IP camera via RTSP using provided credentials
2. It captures a frame from the video stream
3. Computer vision algorithms analyze the frame to detect vertical lines
4. Based on the number of vertical lines detected, the system determines if the gate is open or closed
5. The result is returned via the API

## API Endpoints

### POST /check-gate

Checks the status of a gate using the provided camera credentials.

**Request Body:**
```json
{
  "username": "camera_username",
  "password": "camera_password",
  "ip_address": "camera_ip",
  "port": 554
}
```

**Response:**
```json
{
  "status": "Open",
  "message": "Gate status: Open"
}
```

### GET /health

Simple health check endpoint.

**Response:**
```json
{
  "status": "healthy"
}
```

## Authentication

The API is secured with Bearer token authentication. Set the `API_TOKEN` environment variable to a secure value and include it in the Authorization header of your requests:

```
Authorization: Bearer your-api-token
```

## Installation

### Prerequisites

- Python 3.9+
- OpenCV
- FastAPI
- Uvicorn

### Local Development

1. Clone the repository:
   ```
   git clone https://github.com/gzamboni/open-gate-detector.git
   cd open-gate-detector
   ```

2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Set the API token:
   ```
   export API_TOKEN=your-secure-token
   ```

4. Run the application:
   ```
   python api.py
   ```

The API will be available at http://localhost:8000.

### Running Tests

The project includes comprehensive unit tests with 100% code coverage. To run the tests:

1. Install test dependencies:
   ```
   pip install -r requirements.txt
   ```

2. Run the tests with coverage:
   ```
   pytest --cov=. --cov-report=term
   ```

3. View HTML coverage report:
   ```
   open htmlcov/index.html
   ```

The test suite includes:
- Tests for all gate detector functions with mocked OpenCV dependencies
- API endpoint tests with authentication validation
- Error handling tests

### Docker Deployment

1. Build the Docker image:
   ```
   docker build -t open-gate-detector:latest .
   ```

2. Run the container:
   ```
   docker run -p 8000:8000 -e API_TOKEN=your-secure-token open-gate-detector:latest
   ```

## Kubernetes Deployment

The project includes Kubernetes manifests for deployment:

1. Update the image repository in `k8s/deployment.yaml`
2. Update the Git repository URL in `k8s/argocd-application.yaml`
3. Apply the ArgoCD application:
   ```
   kubectl apply -f k8s/argocd-application.yaml
   ```

## Configuration

The following environment variables can be configured:

- `API_TOKEN`: Authentication token for API access (default: "default-secure-token")

## Technical Details

### Gate Detection Algorithm

The gate detection algorithm works by:

1. Converting the captured frame to grayscale
2. Applying Canny edge detection to identify edges
3. Using Hough Line Transform to detect lines in the image
4. Counting the number of vertical lines (gates typically have vertical bars when closed)
5. Determining gate status based on the number of vertical lines detected

## License

[MIT License](LICENSE)

## Contributing

Contributions are welcome! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines and instructions. For security-related issues, please refer to our [Security Policy](SECURITY.md).

## GitHub Configuration

This repository includes several GitHub-specific configurations:

- **Issue Templates**: Templates for bug reports and feature requests
- **Pull Request Template**: Standard template for pull requests
- **Dependabot**: Automated dependency updates for Python packages, GitHub Actions, and Docker
- **CODEOWNERS**: Defines code ownership and review requirements
- **Workflows**: CI/CD pipelines for testing, linting, and security scanning
