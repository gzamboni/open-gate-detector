"""
Configuration management for the application.

This module handles loading and providing access to configuration settings
from environment variables and other sources.
"""
import os
from typing import Dict, Any


class Settings:
    """Application settings loaded from environment variables."""

    def __init__(self):
        """Initialize settings with default values and load from environment."""
        # We'll use properties to dynamically load values from environment
        pass

    @property
    def api_token(self):
        """Get the current API token from environment."""
        return os.environ.get("API_TOKEN", "default-secure-token")

    @property
    def host(self):
        """Get the host from environment."""
        return os.environ.get("HOST", "0.0.0.0")

    @property
    def port(self):
        """Get the port from environment."""
        return int(os.environ.get("PORT", "8000"))

    @property
    def rtsp_format(self):
        """Get the RTSP format from environment."""
        return os.environ.get(
            "RTSP_FORMAT",
            "rtsp://{username}:{password}@{ip_address}:{port}/cam/realmonitor?channel=8&subtype=0&unicast=true&proto=Onvif"
        )

    @property
    def debug(self):
        """Get the debug setting from environment."""
        return os.environ.get("DEBUG", "").lower() in ("true", "1", "t", "yes")

    @property
    def line_threshold(self):
        """Get the line threshold from environment."""
        return int(os.environ.get("LINE_THRESHOLD", "10"))

        # Server settings
        self.host = os.environ.get("HOST", "0.0.0.0")
        self.port = int(os.environ.get("PORT", "8000"))

        # RTSP settings
        self.rtsp_format = os.environ.get(
            "RTSP_FORMAT",
            "rtsp://{username}:{password}@{ip_address}:{port}/cam/realmonitor?channel=8&subtype=0&unicast=true&proto=Onvif"
        )

        # Application settings
        self.debug = os.environ.get("DEBUG", "").lower() in ("true", "1", "t", "yes")

        # Gate detector settings
        self.line_threshold = int(os.environ.get("LINE_THRESHOLD", "10"))

    def dict(self) -> Dict[str, Any]:
        """Return settings as a dictionary."""
        return {
            "api_token": self.api_token,
            "host": self.host,
            "port": self.port,
            "rtsp_format": self.rtsp_format,
            "debug": self.debug,
            "line_threshold": self.line_threshold,
        }


# Create a global settings instance
settings = Settings()
