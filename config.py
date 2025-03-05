# config.py

# Authentication settings
API_KEY = "secret123"  # Your chosen API key

# Rate limiting settings
RATE_LIMIT_WINDOW = 60  # seconds
RATE_LIMIT_MAX_REQUESTS = 5  # per window per IP

# (Optional) Target backend API URL for forwarding
TARGET_API_URL = "http://127.0.0.1:9000"  # Change if needed

#Redis port
REDIS_PORT = 6379

