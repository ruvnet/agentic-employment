from pydantic import BaseModel, Field
from typing import List, Optional
from enum import Enum
from datetime import datetime

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

class AgentInteraction(BaseModel):
    agent1: str
    agent2: str
    interaction_type: InteractionType
    description: str
    status: InteractionStatus
    timestamp: datetime = Field(default_factory=datetime.now)

class ChatMessage(BaseModel):
    agent: str
    message: str
    timestamp: datetime = Field(default_factory=datetime.now)

class AgentTeam(BaseModel):
    name: str
    members: List[str]
    goal: str

class DeploymentPattern(str, Enum):
    CENTRALIZED = "Centralized"
    DECENTRALIZED = "Decentralized"
    HYBRID = "Hybrid"
    MICROSERVICES = "Microservices"
    SERVERLESS = "Serverless"

class LearningMethod(str, Enum):
    REINFORCEMENT_LEARNING = "Reinforcement Learning"
    SUPERVISED_LEARNING = "Supervised Learning"
    UNSUPERVISED_LEARNING = "Unsupervised Learning"
    TRANSFER_LEARNING = "Transfer Learning"
    CONTINUAL_LEARNING = "Continual Learning"

class EvolutionStrategy(str, Enum):
    GENETIC_ALGORITHMS = "Genetic Algorithms"
    EVOLUTIONARY_STRATEGIES = "Evolutionary Strategies"
    NEUROEVOLUTION = "Neuroevolution"
    LAMARCKIAN_EVOLUTION = "Lamarckian Evolution"
    BALDWINIAN_EVOLUTION = "Baldwinian Evolution"

class HiveStructure(str, Enum):
    HIERARCHICAL = "Hierarchical"
    FLAT = "Flat"
    MATRIX = "Matrix"
    NETWORK = "Network"
    SWARM = "Swarm"

class AgentSystemDeployment(BaseModel):
    deployment_pattern: DeploymentPattern
    learning_method: LearningMethod
    evolution_strategy: EvolutionStrategy
    hive_structure: HiveStructure
    self_orchestration_level: int = Field(..., ge=0, le=100)

class CollaborationGovernance(BaseModel):
    interactions: List[AgentInteraction]
    chat_history: List[ChatMessage]
    teams: List[AgentTeam]
    current_deployment: AgentSystemDeployment

# Example usage:
example_governance = CollaborationGovernance(
    interactions=[
        AgentInteraction(
            agent1="Sales AI",
            agent2="Support Bot",
            interaction_type=InteractionType.COLLABORATION_REQUEST,
            description="Help with customer issue",
            status=InteractionStatus.IN_PROGRESS
        )
    ],
    chat_history=[
        ChatMessage(agent="Sales AI", message="Hey Support Bot, I noticed a customer had an issue with their order. Can you help me understand what happened?"),
        ChatMessage(agent="Support Bot", message="Sure thing, Sales AI! It looks like the customer's order was delayed due to an inventory issue. I've already reached out to them to apologize and offer a discount on their next purchase.")
    ],
    teams=[
        AgentTeam(
            name="Sales Team",
            members=["Sales AI", "Support Bot", "Marketing Assistant"],
            goal="Improve customer acquisition and retention"
        )
    ],
    current_deployment=AgentSystemDeployment(
        deployment_pattern=DeploymentPattern.HYBRID,
        learning_method=LearningMethod.CONTINUAL_LEARNING,
        evolution_strategy=EvolutionStrategy.NEUROEVOLUTION,
        hive_structure=HiveStructure.NETWORK,
        self_orchestration_level=75
    )
)

print(example_governance.json(indent=2))
