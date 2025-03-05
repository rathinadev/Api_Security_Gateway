from fastapi import FastAPI
from middleware import security_gateway_middleware
from routes import router

app = FastAPI()

# Register the middleware (note that the decorator syntax in main.py isn’t used here)
app.middleware("http")(security_gateway_middleware)

# Include the routes defined in routes.py
app.include_router(router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
