import cv2
import numpy as np

# Default RTSP URI format
DEFAULT_RTSP_FORMAT = "rtsp://{username}:{password}@{ip_address}:{port}/cam/realmonitor?channel=8&subtype=0&unicast=true&proto=Onvif"

def get_rtsp_uri(username, password, ip_address, port=554):
    """
    Constructs an RTSP URI from the given parameters.
    """
    return DEFAULT_RTSP_FORMAT.format(
        username=username,
        password=password,
        ip_address=ip_address,
        port=port
    )

def capture_frame(rtsp_uri):
    """
    Captures a snapshot from the given RTSP URI.
    """
    cap = cv2.VideoCapture(rtsp_uri)
    if not cap.isOpened():
        print("Error: Could not open RTSP stream.")
        return None

    ret, snapshot = cap.read()
    cap.release()

    if not ret:
        print("Error: Could not read snapshot from RTSP stream.")
        return None

    return snapshot

def detect_gate_status(snapshot):
    """
    Detects if the gate in the snapshot is open or closed using the Hough Line Transform.
    """

    gray = cv2.cvtColor(snapshot, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, 50, 150, apertureSize=3)

    lines = cv2.HoughLines(edges, 1, np.pi / 180, 200)

    num_vertical_lines = 0
    if lines is not None:
        for _, theta in lines[:, 0]:
            # Filter for vertical lines (theta is close to 0 or pi)
            if np.abs(theta) < np.pi / 180 * 10 or np.abs(theta - np.pi) < np.pi / 180 * 10:
                num_vertical_lines += 1

    # Define a threshold for the number of vertical lines
    line_threshold = 10

    if num_vertical_lines > line_threshold:
        return "Closed"
    else:
        return "Open"

def check_gate_status(username, password, ip_address, port=554):
    """
    Main function to check the gate status with the given credentials.
    Returns a tuple of (status, message).
    """
    rtsp_uri = get_rtsp_uri(username, password, ip_address, port)
    snapshot = capture_frame(rtsp_uri)

    if snapshot is not None:
        status = detect_gate_status(snapshot)
        return status, f"Gate status: {status}"
    else:
        return None, "Error: Could not capture snapshot from RTSP stream."

