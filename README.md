
# Project Title

A brief description of what this project does and who it's for



# API Security Gateway

A modular API Security Gateway built with FastAPI that provides centralized security for your applications. It enforces authentication, rate limiting (using Redis), and request forwarding to a backend API, while also handling designated local endpoints directly.

---

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [Future Enhancements](#future-enhancements)
- [Contributing](#contributing)
- [License](#license)

---

## Overview

The API Security Gateway is designed to sit between clients and your backend API(s). It secures your APIs by:

- **Authenticating** requests using a configurable API key.
- **Rate limiting** requests per client IP using Redis, ensuring persistence and scalability.
- **Forwarding** validated requests to the backend API while converting responses into FastAPI-compatible responses.
- **Handling local endpoints** (such as health checks) directly within the gateway for quick diagnostics and administration.

This approach allows for flexible, centralized security management, reducing redundancy and streamlining your API architecture.

---

## Features

- **Authentication:**  
  Validates requests using an API key supplied in the `x-api-key` header.

- **Redis-Based Rate Limiting:**  
  Limits the number of requests per client IP over a configurable time window, ensuring that excessive usage is controlled and persistent across restarts.

- **Request Forwarding:**  
  Proxies incoming requests to a designated backend API, converting the backend's response into a format that FastAPI can return to the client.

- **Local Endpoint Handling:**  
  Supports selective routing so that certain endpoints (e.g., `/` or `/health`) can be served directly by the gateway rather than being forwarded.

- **Logging:**  
  Logs incoming requests and errors for easier debugging and monitoring.

---

## Project Structure

```
api_gateway_project/
├── main.py           # Initializes FastAPI, registers middleware, and includes routes.
├── middleware.py     # Contains security middleware: authentication, rate limiting (Redis), and request forwarding.
├── routes.py         # Defines local endpoints (e.g., "/", "/health") handled directly by the gateway.
├── config.py         # Centralized configuration settings (API key, rate limit parameters, backend URL, etc.).
├── requirements.txt  # Lists project dependencies.
└── README.md         # Project documentation.
```

---

## Installation

### 1. Clone the Repository

```bash
https://github.com/rathinadev/Api_Security_Gateway.git
cd Api_Security_Gateway
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

---

## Configuration

Customize your gateway settings in the `config.py` file. Here you can set:

- **API_KEY:** The expected API key for authentication.
- **RATE_LIMIT_WINDOW:** The time window (in seconds) for rate limiting.
- **RATE_LIMIT_MAX_REQUESTS:** The maximum number of requests allowed per client IP within the time window.
- **TARGET_API_URL:** The base URL of the backend API where valid requests should be forwarded.
- **REDIS_PORT:** (if needed) the port on which your Redis instance is running.

---

## Usage

### Running the Gateway

1. Ensure your backend API is running (e.g., on port 9000).
2. Start the API Security Gateway:

```bash
uvicorn main:app --reload
```

The gateway will be available at [http://127.0.0.1:8000/](http://127.0.0.1:8000/).

### Testing Endpoints

- **Local Endpoints:**  
  Visit endpoints like `/` or `/health` directly to check the gateway’s status.
  
- **Forwarded Endpoints:**  
  Any endpoint not handled locally is proxied to the backend API. Use a tool like `curl` or Postman to send requests with the required `x-api-key` header.

Example using `curl`:

```bash
curl -H "x-api-key: secret123" http://127.0.0.1:8000/your-backend-endpoint
```

---

## Future Enhancements

- **Robust Error Handling:**  
  Improve exception handling for Redis and backend connection errors.

- **Advanced Authentication:**  
  Implement JWT-based authentication for enhanced security and flexibility.

- **Monitoring & Metrics:**  
  Integrate with monitoring tools (e.g., Prometheus, Grafana) for real-time tracking of requests and errors.

- **Admin Dashboard:**  
  Develop a web-based dashboard to monitor traffic, logs, and rate limits.

- **Containerization:**  
  Create a Dockerfile for containerized deployment and easier scalability.

---

## Contributing

Contributions, suggestions, and bug reports are welcome!  
Please fork the repository and submit pull requests, or open issues with your ideas for improvement.

---

## License

This project is licensed under the [MIT License](LICENSE).


