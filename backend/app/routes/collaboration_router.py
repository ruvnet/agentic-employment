from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import List, Optional
from enum import Enum
from datetime import datetime

router = APIRouter(prefix="/collaboration", tags=["collaboration"])

class InteractionType(str, Enum):
    COLLABORATION_REQUEST = "Collaboration Request"
    KNOWLEDGE_SHARE = "Knowledge Share"
    TASK_HANDOFF = "Task Handoff"
    FEEDBACK = "Feedback"
    HIVE_STRUCTURE_UPDATE = "Hive Structure Update"
    EVOLUTIONARY_ADAPTATION = "Evolutionary Adaptation"
    SELF_ORCHESTRATION = "Self-Orchestration"

class InteractionStatus(str, Enum):
    PENDING = "Pending"
    IN_PROGRESS = "In Progress"
    COMPLETED = "Completed"
    ONGOING = "Ongoing"

class InteractionBase(BaseModel):
    agent1_id: int
    agent2_id: int
    interaction_type: InteractionType
    description: str

class InteractionCreate(InteractionBase):
    pass

class Interaction(InteractionBase):
    id: int
    status: InteractionStatus
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

class TeamBase(BaseModel):
    name: str
    members: List[int]  # List of agent IDs
    goal: str

class TeamCreate(TeamBase):
    pass

class Team(TeamBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

# Mock databases
interactions_db = []
teams_db = []

@router.get("/interactions", response_model=List[Interaction])
async def list_interactions():
    return interactions_db

@router.post("/interactions", response_model=Interaction, status_code=201)
async def create_interaction(interaction: InteractionCreate):
    new_interaction = Interaction(
        id=len(interactions_db) + 1,
        **interaction.dict(),
        status=InteractionStatus.PENDING,
        created_at=datetime.now(),
        updated_at=datetime.now()
    )
    interactions_db.append(new_interaction)
    return new_interaction

@router.get("/interactions/{interaction_id}", response_model=Interaction)
async def get_interaction(interaction_id: int):
    interaction = next((i for i in interactions_db if i.id == interaction_id), None)
    if interaction is None:
        raise HTTPException(status_code=404, detail="Interaction not found")
    return interaction

@router.put("/interactions/{interaction_id}", response_model=Interaction)
async def update_interaction(interaction_id: int, status: InteractionStatus):
    interaction = next((i for i in interactions_db if i.id == interaction_id), None)
    if interaction is None:
        raise HTTPException(status_code=404, detail="Interaction not found")
    interaction.status = status
    interaction.updated_at = datetime.now()
    return interaction

@router.get("/teams", response_model=List[Team])
async def list_teams():
    return teams_db

@router.post("/teams", response_model=Team, status_code=201)
async def create_team(team: TeamCreate):
    new_team = Team(
        id=len(teams_db) + 1,
        **team.dict(),
        created_at=datetime.now(),
        updated_at=datetime.now()
    )
    teams_db.append(new_team)
    return new_team

@router.get("/teams/{team_id}", response_model=Team)
async def get_team(team_id: int):
    team = next((t for t in teams_db if t.id == team_id), None)
    if team is None:
        raise HTTPException(status_code=404, detail="Team not found")
    return team

@router.put("/teams/{team_id}", response_model=Team)
async def update_team(team_id: int, team_update: TeamBase):
    team = next((t for t in teams_db if t.id == team_id), None)
    if team is None:
        raise HTTPException(status_code=404, detail="Team not found")
    
    for key, value in team_update.dict().items():
        setattr(team, key, value)
    
    team.updated_at = datetime.now()
    return team

@router.delete("/teams/{team_id}", status_code=204)
async def delete_team(team_id: int):
    team = next((t for t in teams_db if t.id == team_id), None)
    if team is None:
        raise HTTPException(status_code=404, detail="Team not found")
    teams_db.remove(team)
    return None

@router.post("/teams/{team_id}/add-member", response_model=Team)
async def add_team_member(team_id: int, agent_id: int):
    team = next((t for t in teams_db if t.id == team_id), None)
    if team is None:
        raise HTTPException(status_code=404, detail="Team not found")
    if agent_id not in team.members:
        team.members.append(agent_id)
        team.updated_at = datetime.now()
    return team

@router.post("/teams/{team_id}/remove-member", response_model=Team)
async def remove_team_member(team_id: int, agent_id: int):
    team = next((t for t in teams_db if t.id == team_id), None)
    if team is None:
        raise HTTPException(status_code=404, detail="Team not found")
    if agent_id in team.members:
        team.members.remove(agent_id)
        team.updated_at = datetime.now()
    return team
