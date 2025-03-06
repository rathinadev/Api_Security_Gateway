
# API Security Gateway

A modular API Security Gateway built with FastAPI that provides centralized security for your backend APIs. This gateway enforces authentication, rate limiting (using Redis), and request forwarding, while also exposing local endpoints for health checks, metrics, and administration. Additionally, it features structured logging (with JSON logs) and Prometheus monitoring for real-time insights.

---

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [Testing](#testing)
- [Future Enhancements](#future-enhancements)
- [Contributing](#contributing)
- [License](#license)

---

## Overview

The API Security Gateway acts as a protective layer between clients and your backend APIs. It validates incoming requests, applies rate limiting, and proxies approved requests to your backend. Additionally, the gateway handles select local endpoints—such as health checks and metrics—directly. This setup is designed with industry best practices, including:

- **Structured JSON Logging:** Logs are stored in a rotating file and output to the console in JSON format for easy parsing and monitoring.
- **Prometheus Monitoring:** The gateway is instrumented to expose metrics on `/metrics`, allowing integration with Prometheus (and visualization via Grafana).
- **Redis-Based Rate Limiting:** Ensures consistent rate limiting across sessions and instances.
- **Automated and Manual Testing:** Both types of tests are included to help verify the functionality during development.

---

## Features

- **Static API Key Authentication:**  
  Validates requests using a pre-defined API key.
  
- **Redis-Based Rate Limiting:**  
  Limits the number of requests per client IP within a specified time window. Persistent across restarts and scalable.

- **Request Forwarding:**  
  Proxies requests to a backend API while handling responses and errors appropriately.

- **Local Endpoint Handling:**  
  Endpoints such as `/`, `/health`, and `/metrics` are processed by the gateway itself, not forwarded.

- **Structured Logging:**  
  Logs are output in JSON format and stored in a rotating file (`app.log`), providing detailed, structured logs for troubleshooting and monitoring.

- **Prometheus Monitoring:**  
  Automatically instruments your FastAPI application and exposes metrics on `/metrics` for performance monitoring.

- **Testing:**  
  Includes both automated tests (using pytest and FastAPI's TestClient) and a manual test script (using the `requests` library) for comprehensive validation.

---

## Project Structure

```
api_gateway_project/
├── main.py           # Initializes FastAPI, configures structured logging, registers middleware and routes, and exposes metrics.
├── middleware.py     # Contains security middleware for authentication, rate limiting (Redis), and request forwarding.
├── routes.py         # Defines local endpoints (e.g., "/", "/health") served directly by the gateway.
├── config.py         # Centralized configuration settings (API key, rate limit parameters, backend URL, etc.).
├── requirements.txt  # Lists all project dependencies.
├── test_gateway.py   # Automated tests using pytest and FastAPI's TestClient.
└── README.md         # This project documentation.
```

---

## Installation

### 1. Clone the Repository

```bash
git clone <repository_url>
cd api_gateway_project
```

### 2. Create and Activate a Virtual Environment

For macOS/Linux:

```bash
python3 -m venv venv
source venv/bin/activate
```

For Windows (CMD):

```cmd
python -m venv venv
venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

*If you add new dependencies, update the file using:*

```bash
pip freeze > requirements.txt
```

---

## Configuration

Edit `config.py` to set your configuration values:

- **API_KEY:** The API key used for static authentication.
- **RATE_LIMIT_WINDOW:** The time window (in seconds) for rate limiting.
- **RATE_LIMIT_MAX_REQUESTS:** Maximum number of allowed requests per IP per window.
- **TARGET_API_URL:** The base URL for your backend API (e.g., `http://127.0.0.1:9000`).
- **SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES:** (Planned for JWT authentication.)

---

## Usage

### Starting the Services

1. **Start Your Backend API:**  
   Ensure your backend API is running (e.g., on port 9000). For example:
   ```bash
   uvicorn backend:backend_app --port 9000 --reload
   ```

2. **Run the API Security Gateway:**  
   Start the gateway with:
   ```bash
   uvicorn main:app --reload
   ```

### Accessing Endpoints

- **Local Endpoints:**  
  - `/` and `/health`: Served directly by the gateway.
  - `/metrics`: Exposes Prometheus metrics.
  
- **Forwarded Endpoints:**  
  Any other endpoint (e.g., `/data`) is forwarded to your backend API.

- **Authentication:**  
  Requests must include the header `x-api-key: secret123` (or as defined in `config.py`).

Example using curl for a forwarded endpoint:

```bash
curl -H "x-api-key: secret123" http://127.0.0.1:8000/data
```

---

## Testing

### Automated Testing

Run the pytest suite:

```bash
pytest test_gateway.py
```

This will execute tests for:
- Authentication failures.
- Successful request forwarding.
- Rate limiting enforcement.
- Handling of backend failures.

### Manual Testing

You can also run the manual test script (if provided) for ad-hoc testing:

```bash
python test_endpoints.py
```

This script uses the `requests` library to test both your backend API and the gateway.

---

## Future Enhancements

- **Advanced Authentication (JWT):**  
  Replace the static API key with JWT-based authentication for more flexible, user-based security.

- **Admin Dashboard:**  
  Build a dashboard for real-time monitoring and management of the gateway.

- **Enhanced Error Handling:**  
  Improve error handling with retries and better fallback strategies.

- **Containerization:**  
  Create a Dockerfile for easy deployment and scaling of the gateway.

- **CI/CD Integration:**  
  Set up continuous integration to automatically run tests on code changes.

---

## Contributing

Contributions, bug reports, and feature suggestions are welcome!  
Please fork the repository and submit pull requests, or open issues with your ideas.

---

## License

This project is licensed under the [MIT License](LICENSE).
