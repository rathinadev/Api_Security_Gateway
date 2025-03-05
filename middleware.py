import time
import logging
from fastapi import Request
from fastapi.responses import JSONResponse
from config import API_KEY, RATE_LIMIT_WINDOW, RATE_LIMIT_MAX_REQUESTS

# Set up basic logging
logging.basicConfig(level=logging.INFO)

# In-memory store for rate limiting: maps client IP to a list of timestamps
request_counts = {}

async def security_gateway_middleware(request: Request, call_next):
    # Log the incoming request
    logging.info(f"Request: {request.method} {request.url}")

    # --- Authentication ---
    api_key = request.headers.get("x-api-key")
    if not api_key or api_key != API_KEY:
        return JSONResponse(status_code=401, content={"detail": "Unauthorized"})

    # --- Rate Limiting ---
    client_ip = request.client.host
    current_time = time.time()
    window = RATE_LIMIT_WINDOW
    limit = RATE_LIMIT_MAX_REQUESTS

    # Get the list of timestamps for this client or initialize it
    timestamps = request_counts.get(client_ip, [])
    # Keep only the timestamps within the current window
    timestamps = [t for t in timestamps if current_time - t < window]

    if len(timestamps) >= limit:
        return JSONResponse(status_code=429, content={"detail": "Too Many Requests"})

    # Record the current request's timestamp
    timestamps.append(current_time)
    request_counts[client_ip] = timestamps

    # Process the request if all checks pass
    response = await call_next(request)
    return response
