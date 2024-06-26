from pydantic import BaseModel, Field, field_validator
from datetime import datetime
from utils import *
from configurations import AgentConfiguration
from settings import TrainingSettings, OutputSettings

class Agent(BaseModel):
    id: int
    name: str
    type: AgentType
    status: AgentStatus
    performance: float = Field(ge=0.0, le=5.0)
    configuration: AgentConfiguration
    training_settings: TrainingSettings
    output_settings: OutputSettings
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)

    @field_validator('performance')
    def check_performance(cls, v):
        if not 0 <= v <= 5:
            raise ValueError('Performance must be between 0 and 5')
        return round(v, 1)