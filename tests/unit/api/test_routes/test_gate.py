"""
Tests for the gate API routes.

This module contains tests for the gate-related API endpoints.
"""
import pytest
from unittest.mock import patch
from fastapi import status

from app.domain.models import GateStatus


class TestGateAPI:
    """Tests for the gate API endpoints."""

    def test_check_gate_unauthorized(self, test_client):
        """Test gate check endpoint with invalid token."""
        response = test_client.post(
            "/gate/check",
            headers={"Authorization": "Bearer invalid-token"},
            json={
                "username": "test",
                "password": "test",
                "ip_address": "192.168.1.100"
            }
        )
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert "Invalid authentication token" in response.json()["detail"]

    def test_check_gate_missing_auth(self, test_client):
        """Test gate check endpoint with missing authentication."""
        response = test_client.post(
            "/gate/check",
            json={
                "username": "test",
                "password": "test",
                "ip_address": "192.168.1.100"
            }
        )
        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert "Not authenticated" in response.json()["detail"]

    def test_check_gate_success(self, test_client, mock_gate_detector, api_token):
        """Test successful gate check."""
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
                "ip_address": "192.168.1.100"
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
        assert mock_gate_detector.last_credentials.port == 554

    def test_check_gate_with_custom_port(self, test_client, mock_gate_detector, api_token):
        """Test gate check with custom port."""
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
        assert mock_gate_detector.last_credentials.port == 8554

    def test_check_gate_error_handling(self, test_client, mock_gate_detector, api_token):
        """Test error handling in gate check endpoint."""
        # Setup mock to return an error
        mock_gate_detector.status = None
        mock_gate_detector.error = "Test error"

        # Make request
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
        assert "Error checking gate status: Test error" in result["message"]
