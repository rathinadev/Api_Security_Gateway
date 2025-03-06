import pytest
from fastapi.testclient import TestClient
from main import app
from config import RATE_LIMIT_MAX_REQUESTS

client = TestClient(app)

def test_authentication_failure():
    """
    Test that requests without the correct API key return a 401 Unauthorized.
    """
    response = client.get("/data")  # No x-api-key header provided
    assert response.status_code == 401
    assert response.json() == {"detail": "Unauthorized"}

def test_successful_request_forwarding(monkeypatch):
    """
    Simulate a successful backend response by monkeypatching the forward_request function.
    """
    from fastapi.responses import JSONResponse

    async def fake_forward_request(request):
        # Return a simulated successful backend response.
        return JSONResponse(status_code=200, content={"data": "Fake Backend Response"})
    
    # Patch the forward_request function in the middleware module.
    monkeypatch.setattr("middleware.forward_request", fake_forward_request)
    
    headers = {"x-api-key": "secret123"}
    response = client.get("/data", headers=headers)
    assert response.status_code == 200
    assert response.json() == {"data": "Fake Backend Response"}

def test_rate_limiting(monkeypatch):
    """
    Simulate rate limiting by making check_rate_limit always return a value above the limit.
    """
    async def fake_check_rate_limit(client_ip: str) -> int:
        # Simulate that the client has exceeded the rate limit.
        return RATE_LIMIT_MAX_REQUESTS + 1

    # Patch the check_rate_limit function in the middleware module.
    monkeypatch.setattr("middleware.check_rate_limit", fake_check_rate_limit)
    
    headers = {"x-api-key": "secret123"}
    response = client.get("/data", headers=headers)
    assert response.status_code == 429
    assert response.json() == {"detail": "Too Many Requests"}

def test_backend_failure(monkeypatch):
    """
    Simulate a backend failure by monkeypatching forward_request to return a 502 error.
    """
    from fastapi.responses import JSONResponse

    async def fake_forward_request(request):
        return JSONResponse(status_code=502, content={"detail": "Bad Gateway"})

    monkeypatch.setattr("middleware.forward_request", fake_forward_request)
    
    headers = {"x-api-key": "secret123"}
    response = client.get("/data", headers=headers)
    assert response.status_code == 502
    assert response.json() == {"detail": "Bad Gateway"}
