"""
Integration tests for the API.

This module contains integration tests for the API endpoints.
"""
import pytest
from unittest.mock import patch
from fastapi import status

from app.domain.models import GateStatus


class TestAPIIntegration:
    """Integration tests for the API."""

    def test_health_check(self, test_client):
        """Test the health check endpoint."""
        response = test_client.get("/health")
        assert response.status_code == status.HTTP_200_OK
        assert response.json() == {"status": "healthy"}

    def test_gate_check_flow(self, test_client, mock_gate_detector, api_token):
        """Test the complete gate check flow."""
        # Setup mock
        mock_gate_detector.status = GateStatus.OPEN
        mock_gate_detector.error = None

        # Make request
        response = test_client.post(
            "/gate/check",
            headers={"Authorization": f"Bearer {api_token}"},
            json={
                "username": "test",
                "password": "test",
                "ip_address": "192.168.1.100",
                "port": 8554
            }
        )

        # Assertions
        assert response.status_code == status.HTTP_200_OK
        assert response.json() == {
            "status": "Open",
            "message": "Gate status: Open"
        }

        # Verify service was called with correct parameters
        assert mock_gate_detector.last_credentials is not None
        assert mock_gate_detector.last_credentials.username == "test"
        assert mock_gate_detector.last_credentials.password == "test"
        assert mock_gate_detector.last_credentials.ip_address == "192.168.1.100"
        assert mock_gate_detector.last_credentials.port == 8554

        # Test with a different status
        mock_gate_detector.status = GateStatus.CLOSED

        # Make another request
        response = test_client.post(
            "/gate/check",
            headers={"Authorization": f"Bearer {api_token}"},
            json={
                "username": "test",
                "password": "test",
                "ip_address": "192.168.1.100"
            }
        )

        # Assertions
        assert response.status_code == status.HTTP_200_OK
        assert response.json() == {
            "status": "Closed",
            "message": "Gate status: Closed"
        }

        # Test error case
        mock_gate_detector.error = "Connection failed"

        # Make another request
        response = test_client.post(
            "/gate/check",
            headers={"Authorization": f"Bearer {api_token}"},
            json={
                "username": "test",
                "password": "test",
                "ip_address": "192.168.1.100"
            }
        )

        # Assertions
        assert response.status_code == status.HTTP_200_OK
        result = response.json()
        assert result["status"] is None
        assert "Error checking gate status: Connection failed" in result["message"]
