from pydantic import BaseModel, Field, field_validator
from typing import List, Optional
from datetime import datetime
from utils import LLMChoice


class AgentConfiguration(BaseModel):
    description: str
    llm_choice: LLMChoice
    avatar: Optional[str] = None
    prompt: str
    knowledge_base_url: Optional[str] = None
    learning_rate: float = Field(0.01, ge=0.0, le=1.0)
    exploration_rate: float = Field(0.1, ge=0.0, le=1.0)
