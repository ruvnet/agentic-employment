from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import List, Optional
from enum import Enum

router = APIRouter(prefix="/settings", tags=["settings"])

class AgentType(str, Enum):
    CONVERSATIONAL = "Conversational"
    RETRIEVAL_BASED = "Retrieval-based"
    GENERATIVE = "Generative"
    ANALYTICAL = "Analytical"

class AgentSpecialization(str, Enum):
    SALES = "Sales"
    SUPPORT = "Support"
    MARKETING = "Marketing"
    DATA_ANALYSIS = "Data Analysis"
    HR = "HR"

class RewardStructure(str, Enum):
    FIXED = "Fixed"
    VARIABLE = "Variable"
    PERFORMANCE_BASED = "Performance-based"

class UserRole(str, Enum):
    ADMINISTRATOR = "Administrator"
    DEVELOPER = "Developer"
    ANALYST = "Analyst"
    VIEWER = "Viewer"

class AgentParameters(BaseModel):
    default_learning_rate: float = Field(0.1, ge=0.01, le=1.0)
    default_exploration_rate: float = Field(0.1, ge=0.01, le=1.0)
    enabled_agent_types: List[AgentType] = Field(default_factory=lambda: [AgentType.CONVERSATIONAL, AgentType.RETRIEVAL_BASED])
    enabled_agent_specializations: List[AgentSpecialization] = Field(default_factory=lambda: [AgentSpecialization.SALES, AgentSpecialization.SUPPORT])
    reward_structure: RewardStructure = RewardStructure.FIXED
    max_tokens_per_response: int = Field(512, ge=1)

class ResourceManagement(BaseModel):
    max_compute_usage: float = Field(10000, ge=0)  # vCPU hours
    max_storage_usage: float = Field(1000, ge=0)  # GB
    cost_per_compute_hour: float = Field(0.05, ge=0)
    cost_per_gb_storage: float = Field(0.02, ge=0)

class AccessPermissions(BaseModel):
    enabled_user_roles: List[UserRole] = Field(default_factory=lambda: [UserRole.ADMINISTRATOR, UserRole.DEVELOPER])
    enable_api_access: bool = True
    api_rate_limit: int = Field(1000, ge=0)
    enable_logging: bool = True

class SystemSettings(BaseModel):
    agent_parameters: AgentParameters
    resource_management: ResourceManagement
    access_permissions: AccessPermissions

# Global variable to store settings
current_settings = SystemSettings(
    agent_parameters=AgentParameters(),
    resource_management=ResourceManagement(),
    access_permissions=AccessPermissions()
)

@router.get("/", response_model=SystemSettings)
async def get_settings():
    return current_settings

@router.put("/", response_model=SystemSettings)
async def update_settings(settings: SystemSettings):
    global current_settings
    current_settings = settings
    return current_settings

@router.get("/agent-parameters", response_model=AgentParameters)
async def get_agent_parameters():
    return current_settings.agent_parameters

@router.put("/agent-parameters", response_model=AgentParameters)
async def update_agent_parameters(parameters: AgentParameters):
    current_settings.agent_parameters = parameters
    return current_settings.agent_parameters

@router.get("/resource-management", response_model=ResourceManagement)
async def get_resource_management():
    return current_settings.resource_management

@router.put("/resource-management", response_model=ResourceManagement)
async def update_resource_management(resource_management: ResourceManagement):
    current_settings.resource_management = resource_management
    return current_settings.resource_management

@router.get("/access-permissions", response_model=AccessPermissions)
async def get_access_permissions():
    return current_settings.access_permissions

@router.put("/access-permissions", response_model=AccessPermissions)
async def update_access_permissions(permissions: AccessPermissions):
    current_settings.access_permissions = permissions
    return current_settings.access_permissions

@router.post("/reset", response_model=SystemSettings)
async def reset_settings():
    global current_settings
    current_settings = SystemSettings(
        agent_parameters=AgentParameters(),
        resource_management=ResourceManagement(),
        access_permissions=AccessPermissions()
    )
    return current_settings

@router.get("/agent-types", response_model=List[AgentType])
async def get_agent_types():
    return list(AgentType)

@router.get("/agent-specializations", response_model=List[AgentSpecialization])
async def get_agent_specializations():
    return list(AgentSpecialization)

@router.get("/user-roles", response_model=List[UserRole])
async def get_user_roles():
    return list(UserRole)