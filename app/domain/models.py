"""
Domain models for the gate detector application.

These models represent the core business entities and value objects.
"""
from enum import Enum
from dataclasses import dataclass
from typing import Optional


class GateStatus(str, Enum):
    """Enumeration of possible gate statuses."""
    OPEN = "Open"
    CLOSED = "Closed"
    UNKNOWN = "Unknown"


@dataclass
class CameraCredentials:
    """Camera credentials for RTSP connection."""
    username: str
    password: str
    ip_address: str
    port: int = 554

    def get_rtsp_uri(self, format_string: str) -> str:
        """
        Constructs an RTSP URI from the credentials using the provided format string.

        Args:
            format_string: The format string for the RTSP URI.

        Returns:
            The formatted RTSP URI.
        """
        return format_string.format(
            username=self.username,
            password=self.password,
            ip_address=self.ip_address,
            port=self.port
        )


@dataclass
class GateStatusResult:
    """Result of a gate status check."""
    status: Optional[GateStatus] = None
    message: str = ""

    @classmethod
    def success(cls, status: GateStatus) -> "GateStatusResult":
        """
        Create a successful gate status result.

        Args:
            status: The detected gate status.

        Returns:
            A GateStatusResult with the status and a success message.
        """
        return cls(
            status=status,
            message=f"Gate status: {status.value}"
        )

    @classmethod
    def error(cls, error_message: str) -> "GateStatusResult":
        """
        Create an error gate status result.

        Args:
            error_message: The error message.

        Returns:
            A GateStatusResult with no status and an error message.
        """
        return cls(
            status=None,
            message=f"Error checking gate status: {error_message}"
        )
