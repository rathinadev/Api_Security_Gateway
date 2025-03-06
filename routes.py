## Routes that would be taken care by the gateway for its working and monitoring


from fastapi import APIRouter

router = APIRouter()

@router.get("/health")
async def health_check():
    return {"status": "healthy"}

@router.get("/")
async def read_root():
    return {"message": "Welcome to the API Security Gateway!"}
