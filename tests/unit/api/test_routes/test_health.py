"""
Tests for the health API routes.

This module contains tests for the health-related API endpoints.
"""
import pytest
from fastapi import status


class TestHealthAPI:
    """Tests for the health API endpoints."""

    def test_health_check(self, test_client):
        """Test the health check endpoint."""
        response = test_client.get("/health")
        assert response.status_code == status.HTTP_200_OK
        assert response.json() == {"status": "healthy"}
