import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
import os

from api import app, API_TOKEN, GateStatusResponse

# Create a test client
client = TestClient(app)

class TestAPI:
    def setup_method(self):
        """Setup before each test"""
        # Store original API token
        self.original_token = os.environ.get("API_TOKEN")
        # Set a known token for testing
        os.environ["API_TOKEN"] = "test-token"

    def teardown_method(self):
        """Cleanup after each test"""
        # Restore original API token
        if self.original_token:
            os.environ["API_TOKEN"] = self.original_token
        else:
            del os.environ["API_TOKEN"]

    def test_health_check(self):
        """Test the health check endpoint"""
        response = client.get("/health")
        assert response.status_code == 200
        assert response.json() == {"status": "healthy"}

    def test_check_gate_unauthorized(self):
        """Test gate check endpoint with invalid token"""
        response = client.post(
            "/check-gate",
            headers={"Authorization": "Bearer invalid-token"},
            json={
                "username": "test",
                "password": "test",
                "ip_address": "192.168.1.100"
            }
        )
        assert response.status_code == 401
        assert "Invalid authentication token" in response.json()["detail"]

    def test_check_gate_missing_auth(self):
        """Test gate check endpoint with missing authentication"""
        response = client.post(
            "/check-gate",
            json={
                "username": "test",
                "password": "test",
                "ip_address": "192.168.1.100"
            }
        )
        assert response.status_code == 403
        assert "Not authenticated" in response.json()["detail"]

    @patch('api.check_gate_status')
    def test_check_gate_success(self, mock_check_gate):
        """Test successful gate check"""
        # Setup mock
        mock_check_gate.return_value = ("Open", "Gate status: Open")

        # Make request
        response = client.post(
            "/check-gate",
            headers={"Authorization": f"Bearer {API_TOKEN}"},
            json={
                "username": "test",
                "password": "test",
                "ip_address": "192.168.1.100"
            }
        )

        # Assertions
        assert response.status_code == 200
        assert response.json() == {
            "status": "Open",
            "message": "Gate status: Open"
        }
        mock_check_gate.assert_called_once_with(
            "test", "test", "192.168.1.100", 554
        )

    @patch('api.check_gate_status')
    def test_check_gate_with_custom_port(self, mock_check_gate):
        """Test gate check with custom port"""
        # Setup mock
        mock_check_gate.return_value = ("Open", "Gate status: Open")

        # Make request
        response = client.post(
            "/check-gate",
            headers={"Authorization": f"Bearer {API_TOKEN}"},
            json={
                "username": "test",
                "password": "test",
                "ip_address": "192.168.1.100",
                "port": 8554
            }
        )

        # Assertions
        assert response.status_code == 200
        assert response.json() == {
            "status": "Open",
            "message": "Gate status: Open"
        }
        mock_check_gate.assert_called_once_with(
            "test", "test", "192.168.1.100", 8554
        )

    @patch('api.check_gate_status')
    def test_check_gate_error_handling(self, mock_check_gate):
        """Test error handling in gate check endpoint"""
        # Setup mock to raise an exception
        mock_check_gate.side_effect = Exception("Test error")

        # Make request
        response = client.post(
            "/check-gate",
            headers={"Authorization": f"Bearer {API_TOKEN}"},
            json={
                "username": "test",
                "password": "test",
                "ip_address": "192.168.1.100"
            }
        )

        # Assertions
        assert response.status_code == 200  # API returns 200 even for errors
        result = response.json()
        assert result["status"] is None
        assert "Error checking gate status: Test error" in result["message"]
