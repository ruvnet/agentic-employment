from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import List, Optional
from enum import Enum
from datetime import datetime

router = APIRouter(prefix="/agents", tags=["agents"])

# Pydantic models
class AgentType(str, Enum):
    CONVERSATIONAL = "Conversational"
    ANALYTICAL = "Analytical"
    GENERATIVE = "Generative"
    RETRIEVAL_BASED = "Retrieval-based"

class AgentStatus(str, Enum):
    ACTIVE = "Active"
    INACTIVE = "Inactive"

class AgentBase(BaseModel):
    name: str
    type: AgentType
    description: str

class AgentCreate(AgentBase):
    pass

class AgentUpdate(AgentBase):
    status: Optional[AgentStatus] = None

class Agent(AgentBase):
    id: int
    status: AgentStatus
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

# Mock database
agents_db = []

# Helper function to find an agent by ID
def find_agent(agent_id: int):
    return next((agent for agent in agents_db if agent.id == agent_id), None)

@router.get("/", response_model=List[Agent])
async def list_agents():
    return agents_db

@router.post("/", response_model=Agent, status_code=201)
async def create_agent(agent: AgentCreate):
    new_agent = Agent(
        id=len(agents_db) + 1,
        **agent.dict(),
        status=AgentStatus.ACTIVE,
        created_at=datetime.now(),
        updated_at=datetime.now()
    )
    agents_db.append(new_agent)
    return new_agent

@router.get("/{agent_id}", response_model=Agent)
async def get_agent(agent_id: int):
    agent = find_agent(agent_id)
    if agent is None:
        raise HTTPException(status_code=404, detail="Agent not found")
    return agent

@router.put("/{agent_id}", response_model=Agent)
async def update_agent(agent_id: int, agent_update: AgentUpdate):
    agent = find_agent(agent_id)
    if agent is None:
        raise HTTPException(status_code=404, detail="Agent not found")
    
    update_data = agent_update.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(agent, key, value)
    
    agent.updated_at = datetime.now()
    return agent

@router.delete("/{agent_id}", status_code=204)
async def delete_agent(agent_id: int):
    agent = find_agent(agent_id)
    if agent is None:
        raise HTTPException(status_code=404, detail="Agent not found")
    agents_db.remove(agent)
    return None

# Additional endpoint for agent actions
@router.post("/{agent_id}/action", response_model=dict)
async def perform_agent_action(agent_id: int, action: str):
    agent = find_agent(agent_id)
    if agent is None:
        raise HTTPException(status_code=404, detail="Agent not found")
    
    # Here you would implement the logic for different agent actions
    # For now, we'll just return a mock response
    return {"message": f"Action '{action}' performed by agent {agent.name}"}