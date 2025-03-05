from fastapi import APIRouter

router = APIRouter()

@router.get("/")
async def read_root():
    return {"message": "Welcome to the API Security Gateway!"}
