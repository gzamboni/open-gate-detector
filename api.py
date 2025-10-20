import uvicorn
from fastapi import FastAPI, Depends, HTTPException, status, Header
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
from typing import Optional
import os
from fastapi.responses import JSONResponse

from gate_detector import check_gate_status

app = FastAPI(title="Gate Status API", description="API to check if a gate is open or closed")
security = HTTPBearer()

# Get API token from environment variable
API_TOKEN = os.environ.get("API_TOKEN", "default-secure-token")

class GateCheckRequest(BaseModel):
    """Request model for gate status check"""
    username: str
    password: str
    ip_address: str
    port: Optional[int] = 554

class GateStatusResponse(BaseModel):
    """Response model for gate status"""
    status: Optional[str] = None
    message: str

# Simple Bearer token authentication
def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """Simple Bearer token authentication for the API"""
    if credentials.credentials != API_TOKEN:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return True

@app.post("/check-gate", response_model=GateStatusResponse)
def check_gate(
    request: GateCheckRequest,
    authenticated: bool = Depends(verify_token)
):
    """
    Check if the gate is open or closed

    This endpoint requires:
    - API authentication (Bearer Token from API_TOKEN environment variable)
    - Camera credentials and IP in the request body
    """
    try:
        # Call the gate detector function with the provided parameters
        # Ensure port is not None before passing to check_gate_status
        port = request.port if request.port is not None else 554

        gate_status, message = check_gate_status(
            request.username,
            request.password,
            request.ip_address,
            port
        )

        return GateStatusResponse(
            status=gate_status,
            message=message
        )
    except Exception as e:
        return GateStatusResponse(
            status=None,
            message=f"Error checking gate status: {str(e)}"
        )

@app.get("/health")
def health_check():
    """Simple health check endpoint"""
    return {"status": "healthy"}

if __name__ == "__main__":
    # Run the API server
    uvicorn.run("api:app", host="0.0.0.0", port=8000, reload=True)
