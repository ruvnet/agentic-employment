from enum import Enum
from typing import List
from pydantic import BaseModel, Field


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



class TrainingSettings(BaseModel):
    iterations: int = Field(10, ge=1, le=100)
    batch_size: int = Field(32, ge=1, le=256)

class OutputSettings(BaseModel):
    max_tokens: int = Field(512, ge=1, le=4096)
    temperature: float = Field(0.7, ge=0.0, le=1.0)
    top_p: float = Field(1.0, ge=0.0, le=1.0)
    frequency_penalty: float = Field(0.0, ge=0.0, le=2.0)
    presence_penalty: float = Field(0.0, ge=0.0, le=2.0)
    stop_sequences: List[str] = Field(default_factory=list)
    