#The actual backend api our proxy protects

# Run at port 9000

from fastapi import FastAPI

backend_app = FastAPI()

@backend_app.get("/data")
async def get_data():
    return {"data": "Response from backend API"}
