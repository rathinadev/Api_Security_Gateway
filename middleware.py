import time
import httpx
import logging
from fastapi import Request, Response
from fastapi.responses import JSONResponse
from config import API_KEY, RATE_LIMIT_WINDOW, RATE_LIMIT_MAX_REQUESTS, TARGET_API_URL
import redis.asyncio as redis  # Using the asyncio version of Redis

# Set up basic logging
logging.basicConfig(level=logging.INFO)

# Create an asynchronous Redis client
redis_client = redis.Redis(host='localhost', port=6379, decode_responses=True)

async def check_rate_limit(client_ip: str) -> int:
    """
    Increments the request counter for a client IP in Redis.
    Returns the current count after increment.
    Sets the key to expire after RATE_LIMIT_WINDOW seconds if it doesn't already exist.
    """
    key = f"rate_limit:{client_ip}"
    try:
        current = await redis_client.incr(key)
        if current == 1:
            # If this is the first request, set the expiration time
            await redis_client.expire(key, RATE_LIMIT_WINDOW)
        return current
    except Exception as e:
        logging.error(f"Redis error for IP {client_ip}: {e}")
        # Optionally, you might allow the request to pass in case of Redis failure,
        # or you could choose to block the request. Here, we choose to allow it.
        return 0

async def forward_request(request: Request):
    try:
        async with httpx.AsyncClient() as client:
            backend_response = await client.request(
                method=request.method,
                url=f"{TARGET_API_URL}{request.url.path}",
                headers=dict(request.headers),
                content=await request.body()
            )
    except Exception as e:
        logging.error(f"Error forwarding request: {e}")
        # Return a 502 Bad Gateway if the request to the backend fails.
        return JSONResponse(status_code=502, content={"detail": "Bad Gateway"})

    # Determine content type and return an appropriate FastAPI response.
    content_type = backend_response.headers.get("content-type", "")
    if "application/json" in content_type:
        try:
            # If the response is JSON, return a JSONResponse.
            return JSONResponse(
                status_code=backend_response.status_code,
                content=backend_response.json(),
                headers=dict(backend_response.headers)
            )
        except Exception as e:
            logging.error(f"Error processing JSON response: {e}")
            return JSONResponse(status_code=500, content={"detail": "Error processing JSON response"})
    else:
        return Response(
            content=backend_response.content,
            status_code=backend_response.status_code,
            headers=dict(backend_response.headers)
        )

async def security_gateway_middleware(request: Request, call_next):
    # Log the incoming request
    logging.info(f"Request: {request.method} {request.url}")

    # --- Authentication ---
    api_key = request.headers.get("x-api-key")
    if not api_key or api_key != API_KEY:
        return JSONResponse(status_code=401, content={"detail": "Unauthorized"})

    # --- Rate Limiting using Redis ---
    client_ip = request.client.host
    current_count = await check_rate_limit(client_ip)
    if current_count > RATE_LIMIT_MAX_REQUESTS:
        return JSONResponse(status_code=429, content={"detail": "Too Many Requests"})
    
    # Decide whether to forward or let FastAPI handle it
    if request.url.path in ["/", "/health","/metrics"]:
        # Let FastAPI's router (i.e., routes.py) handle these endpoints
        return await call_next(request)

    # Process the request if all checks pass by forwarding it
    response = await forward_request(request)
    return response
