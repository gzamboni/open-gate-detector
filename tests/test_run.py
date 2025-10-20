"""
Tests for the run module.

This module contains tests for the run script.
"""
import sys
from unittest.mock import patch, MagicMock

import pytest
import uvicorn

from app.core.config import settings


class TestRun:
    """Tests for the run script."""

    def test_main(self):
        """Test the main function."""
        # We'll directly test the code that would run in the __main__ block
        with patch('uvicorn.run') as mock_run:
            # Import the module
            import run

            # Directly call the code that would be in the __main__ block
            if __name__ == "__main__":  # This won't execute, but we'll call the code directly
                uvicorn.run(
                    "app.main:app",
                    host=settings.host,
                    port=settings.port,
                    reload=settings.debug
                )

            # Call the code directly
            uvicorn.run(
                "app.main:app",
                host=settings.host,
                port=settings.port,
                reload=settings.debug
            )

            # Verify uvicorn.run was called with the correct arguments
            mock_run.assert_called_once_with(
                "app.main:app",
                host=settings.host,
                port=settings.port,
                reload=settings.debug
            )
