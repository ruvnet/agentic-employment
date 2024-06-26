from pydantic import BaseModel, Field
from typing import List, Optional
from enum import Enum
from datetime import date, datetime

class ReportType(str, Enum):
    AGENT_ACTIVITIES = "Agent Activities"
    AGENT_OUTPUTS = "Agent Outputs"
    QUALITY_LEVELS = "Quality Levels"

class ReportPeriod(str, Enum):
    LAST_7_DAYS = "Last 7 Days"
    LAST_30_DAYS = "Last 30 Days"
    LAST_6_MONTHS = "Last 6 Months"
    LAST_YEAR = "Last Year"
    CUSTOM_RANGE = "Custom Range"

class ForecastMetric(str, Enum):
    TOTAL_AGENTS = "Total Agents"
    ACTIVE_AGENTS = "Active Agents"
    TASKS_COMPLETED = "Tasks Completed"
    AVG_RATING = "Avg Rating"

class ForecastPeriod(str, Enum):
    NEXT_7_DAYS = "Next 7 Days"
    NEXT_30_DAYS = "Next 30 Days"
    NEXT_6_MONTHS = "Next 6 Months"
    NEXT_YEAR = "Next Year"

class AgentMetrics(BaseModel):
    date: date
    total_agents: int
    active_agents: int
    tasks_completed: int
    avg_rating: float = Field(..., ge=0, le=5)

class AgentTeamMetrics(BaseModel):
    team: str
    agents: int
    tasks: int
    avg_rating: float = Field(..., ge=0, le=5)

class AgentReport(BaseModel):
    agent: str
    tasks_completed: int
    success_rate: float = Field(..., ge=0, le=100)
    avg_rating: float = Field(..., ge=0, le=5)

class ReportRequest(BaseModel):
    report_type: ReportType
    report_period: ReportPeriod
    start_date: Optional[date] = None
    end_date: Optional[date] = None

class ForecastRequest(BaseModel):
    metric: ForecastMetric
    period: ForecastPeriod

class ForecastData(BaseModel):
    date: date
    value: float

class Analytics(BaseModel):
    agent_metrics: List[AgentMetrics]
    agent_teams: List[AgentTeamMetrics]

class Report(BaseModel):
    report_type: ReportType
    period: ReportPeriod
    start_date: date
    end_date: date
    data: List[AgentReport]

class Forecast(BaseModel):
    metric: ForecastMetric
    period: ForecastPeriod
    data: List[ForecastData]
