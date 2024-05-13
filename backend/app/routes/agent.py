from fastapi import APIRouter

router = APIRouter()

@router.get("/agents")
async def get_agents():
    return {"message": "List of agents"}
