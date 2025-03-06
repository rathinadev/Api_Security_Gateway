import logging
from pythonjsonlogger import jsonlogger
from logging.handlers import RotatingFileHandler
from fastapi import FastAPI
from middleware import security_gateway_middleware
from routes import router

# ================================
# Structured Logging Configuration
# ================================

# Create and configure the root logger
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Create a rotating file handler:
# - Logs will be stored in 'app.log'
# - Each log file is capped at 10 MB
# - Up to 5 backup files will be kept
file_handler = RotatingFileHandler("app.log", maxBytes=10 * 1024 * 1024, backupCount=5)

# Define a JSON formatter that outputs essential fields
formatter = jsonlogger.JsonFormatter('%(asctime)s %(levelname)s %(name)s %(message)s')
file_handler.setFormatter(formatter)

# Add the file handler to the logger
logger.addHandler(file_handler)

# Also add a console handler to output logs to stdout
console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)

# Log an initial message to confirm the setup
logger.info("Structured logging configured. Logs will be stored in app.log and output to the console.")

# ================================
# FastAPI Application Setup
# ================================

app = FastAPI()

# Register the security middleware (which handles authentication, rate limiting, and request forwarding)
app.middleware("http")(security_gateway_middleware)

# Include local routes defined in routes.py (for example, health check endpoints)
app.include_router(router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
