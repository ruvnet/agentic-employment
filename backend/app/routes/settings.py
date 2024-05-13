from fastapi import APIRouter

router = APIRouter()

@router.get("/settings")
async def get_settings():
    return {"message": "Settings page"}
