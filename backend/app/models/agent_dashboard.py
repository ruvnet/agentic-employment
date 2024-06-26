from pydantic import BaseModel

class AgentDashboard(BaseModel):
    total_agents: int
    active_agents: int
    idle_agents: int
    total_tasks_completed: int
    avg_task_duration: float
    avg_agent_rating: float
    compute_usage: float
    storage_usage: float
    total_llm_calls: int
    total_cost: float
    cost_per_task: float
    budget_remaining: float