"""
Tests for the configuration module.

This module contains tests for the configuration settings.
"""
import os
from unittest.mock import patch

from app.core.config import Settings


class TestSettings:
    """Tests for the Settings class."""

    def test_api_token_property(self):
        """Test the api_token property."""
        # Create settings
        settings = Settings()

        # Test with default value
        with patch.dict(os.environ, {}, clear=True):
            assert settings.api_token == "default-secure-token"

        # Test with environment variable
        with patch.dict(os.environ, {"API_TOKEN": "test-token"}, clear=True):
            assert settings.api_token == "test-token"

    def test_host_property(self):
        """Test the host property."""
        # Create settings
        settings = Settings()

        # Test with no environment variable - should be None
        with patch.dict(os.environ, {}, clear=True):
            assert settings.host is None

        # Test with environment variable
        with patch.dict(os.environ, {"HOST": "localhost"}, clear=True):
            assert settings.host == "localhost"

    def test_port_property(self):
        """Test the port property."""
        # Create settings
        settings = Settings()

        # Test with default value
        with patch.dict(os.environ, {}, clear=True):
            assert settings.port == 8000

        # Test with environment variable
        with patch.dict(os.environ, {"PORT": "9000"}, clear=True):
            assert settings.port == 9000

    def test_rtsp_format_property(self):
        """Test the rtsp_format property."""
        # Create settings
        settings = Settings()

        # Test with default value
        with patch.dict(os.environ, {}, clear=True):
            assert "rtsp://{username}:{password}@{ip_address}:{port}" in settings.rtsp_format

        # Test with environment variable
        custom_format = "rtsp://{ip_address}:{port}"
        with patch.dict(os.environ, {"RTSP_FORMAT": custom_format}, clear=True):
            assert settings.rtsp_format == custom_format

    def test_debug_property(self):
        """Test the debug property."""
        # Create settings
        settings = Settings()

        # Test with default value
        with patch.dict(os.environ, {}, clear=True):
            assert settings.debug is False

        # Test with environment variable
        with patch.dict(os.environ, {"DEBUG": "true"}, clear=True):
            assert settings.debug is True

        with patch.dict(os.environ, {"DEBUG": "1"}, clear=True):
            assert settings.debug is True

        with patch.dict(os.environ, {"DEBUG": "false"}, clear=True):
            assert settings.debug is False

    def test_line_threshold_property(self):
        """Test the line_threshold property."""
        # Create settings
        settings = Settings()

        # Test with default value
        with patch.dict(os.environ, {}, clear=True):
            assert settings.line_threshold == 10

        # Test with environment variable
        with patch.dict(os.environ, {"LINE_THRESHOLD": "20"}, clear=True):
            assert settings.line_threshold == 20

    def test_dict_method(self):
        """Test the dict method."""
        # Create settings
        settings = Settings()

        # Test with default values
        with patch.dict(os.environ, {}, clear=True):
            settings_dict = settings.dict()
            assert settings_dict["api_token"] == "default-secure-token"
            assert settings_dict["host"] is None
            assert settings_dict["port"] == 8000
            assert "rtsp://{username}:{password}@{ip_address}:{port}" in settings_dict["rtsp_format"]
            assert settings_dict["debug"] is False
            assert settings_dict["line_threshold"] == 10
