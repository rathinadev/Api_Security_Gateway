## Python file to test both backend  API and Gateway API


import requests
import time

# URLs for your backend API and your gateway
GATEWAY_URL = "http://127.0.0.1:8000"
BACKEND_URL = "http://127.0.0.1:9000"

# Headers for authenticated requests (ensure this matches your API_KEY in config.py)
AUTH_HEADERS = {"x-api-key": "secret123"}

def test_backend():
    """Test the backend API directly."""
    print("=== Testing Backend API Directly ===")
    try:
        response = requests.get(f"{BACKEND_URL}/data")
        print("Backend Status Code:", response.status_code)
        print("Backend Response:", response.json())
    except Exception as e:
        print("Error testing backend API:", e)
    print()

def test_gateway_forward():
    """Test the gateway forwarding a request to the backend API."""
    print("=== Testing Gateway Forwarding ===")
    try:
        response = requests.get(f"{GATEWAY_URL}/data", headers=AUTH_HEADERS)
        print("Gateway Forward Status Code:", response.status_code)
        try:
            print("Gateway Forward Response (JSON):", response.json())
        except Exception:
            print("Gateway Forward Response (raw):", response.text)
    except Exception as e:
        print("Error testing gateway forwarding:", e)
    print()

def test_gateway_local():
    """
    Test a local endpoint handled by the gateway.
    For example, if you have a /health endpoint defined in routes.py.
    """
    print("=== Testing Gateway Local Endpoint (/health) ===")
    try:
        response = requests.get(f"{GATEWAY_URL}/health", headers=AUTH_HEADERS)
        print("Local Endpoint Status Code:", response.status_code)
        try:
            print("Local Endpoint Response (JSON):", response.json())
        except Exception:
            print("Local Endpoint Response (raw):", response.text)
    except Exception as e:
        print("Error testing local endpoint:", e)
    print()

def test_auth_failure():
    """Test the gateway's authentication failure (missing API key)."""
    print("=== Testing Gateway Authentication Failure ===")
    try:
        # Do not pass the authentication header.
        response = requests.get(f"{GATEWAY_URL}/data")
        print("Auth Failure Status Code:", response.status_code)
        try:
            print("Auth Failure Response (JSON):", response.json())
        except Exception:
            print("Auth Failure Response (raw):", response.text)
    except Exception as e:
        print("Error testing auth failure:", e)
    print()

def test_rate_limiting():
    """
    Test the gateway's rate limiting by making several quick requests.
    Adjust the loop count based on your RATE_LIMIT_MAX_REQUESTS setting.
    """
    print("=== Testing Gateway Rate Limiting ===")
    for i in range(10):  # sending 10 requests in rapid succession
        try:
            response = requests.get(f"{GATEWAY_URL}/data", headers=AUTH_HEADERS)
            print(f"Request {i+1}: Status Code: {response.status_code}")
        except Exception as e:
            print(f"Error on request {i+1}:", e)
        time.sleep(0.5)  # short delay; adjust as needed
    print()

if __name__ == "__main__":
    print("Starting tests...\n")
    
    # Test backend API directly (ensure your backend is running on port 9000)
    test_backend()

    # Test the gateway forwarding behavior (this should proxy to your backend)
    test_gateway_forward()

    # Test a local endpoint served directly by the gateway.
    # Ensure you have defined such an endpoint in routes.py (e.g., /health).
    test_gateway_local()

    # Test authentication failure by not providing the API key
    test_auth_failure()

    # Test rate limiting by sending multiple requests rapidly.
    test_rate_limiting()

    print("Tests completed.")
