from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel
from typing import List, Optional
from enum import Enum
from datetime import date, datetime

router = APIRouter(prefix="/analytics", tags=["analytics"])

class MetricType(str, Enum):
    TOTAL_AGENTS = "Total Agents"
    ACTIVE_AGENTS = "Active Agents"
    TASKS_COMPLETED = "Tasks Completed"
    AVG_RATING = "Average Rating"

class ReportType(str, Enum):
    AGENT_ACTIVITIES = "Agent Activities"
    AGENT_OUTPUTS = "Agent Outputs"
    QUALITY_LEVELS = "Quality Levels"

class ForecastMetric(str, Enum):
    TOTAL_AGENTS = "Total Agents"
    ACTIVE_AGENTS = "Active Agents"
    TASKS_COMPLETED = "Tasks Completed"
    AVG_RATING = "Average Rating"

class Metric(BaseModel):
    type: MetricType
    value: float
    date: date

class Report(BaseModel):
    type: ReportType
    data: List[dict]
    generated_at: datetime

class Forecast(BaseModel):
    metric: ForecastMetric
    predictions: List[dict]
    generated_at: datetime

@router.get("/metrics", response_model=List[Metric])
async def get_metrics(
    metric_type: Optional[MetricType] = None,
    start_date: Optional[date] = None,
    end_date: Optional[date] = None
):
    # In a real application, you would fetch this data from a database
    # Here, we're returning mock data
    mock_metrics = [
        Metric(type=MetricType.TOTAL_AGENTS, value=100, date=date(2023, 6, 1)),
        Metric(type=MetricType.ACTIVE_AGENTS, value=80, date=date(2023, 6, 1)),
        Metric(type=MetricType.TASKS_COMPLETED, value=500, date=date(2023, 6, 1)),
        Metric(type=MetricType.AVG_RATING, value=4.5, date=date(2023, 6, 1)),
    ]
    
    if metric_type:
        mock_metrics = [m for m in mock_metrics if m.type == metric_type]
    if start_date:
        mock_metrics = [m for m in mock_metrics if m.date >= start_date]
    if end_date:
        mock_metrics = [m for m in mock_metrics if m.date <= end_date]
    
    return mock_metrics

@router.get("/reports", response_model=Report)
async def generate_report(report_type: ReportType):
    # In a real application, you would generate this report based on actual data
    # Here, we're returning mock data
    mock_report = Report(
        type=report_type,
        data=[
            {"agent": "Agent 1", "tasks_completed": 100, "avg_rating": 4.5},
            {"agent": "Agent 2", "tasks_completed": 150, "avg_rating": 4.2},
            {"agent": "Agent 3", "tasks_completed": 80, "avg_rating": 4.8},
        ],
        generated_at=datetime.now()
    )
    return mock_report

@router.get("/forecasts", response_model=Forecast)
async def generate_forecast(
    metric: ForecastMetric,
    days: int = Query(default=30, ge=1, le=365)
):
    # In a real application, you would generate this forecast based on historical data and a forecasting model
    # Here, we're returning mock data
    mock_forecast = Forecast(
        metric=metric,
        predictions=[
            {"date": date(2023, 7, 1), "value": 110},
            {"date": date(2023, 7, 2), "value": 115},
            {"date": date(2023, 7, 3), "value": 120},
            # ... more predictions ...
        ],
        generated_at=datetime.now()
    )
    return mock_forecast

@router.get("/performance", response_model=dict)
async def get_performance_metrics(
    agent_id: Optional[int] = None,
    start_date: Optional[date] = None,
    end_date: Optional[date] = None
):
    # In a real application, you would fetch this data from a database
    # Here, we're returning mock data
    mock_performance = {
        "tasks_completed": 500,
        "avg_response_time": 1.5,  # in seconds
        "avg_rating": 4.7,
        "success_rate": 0.95
    }
    return mock_performance

@router.get("/agent-comparison", response_model=List[dict])
async def compare_agents(agent_ids: List[int] = Query(...)):
    # In a real application, you would fetch and compare data for the specified agents
    # Here, we're returning mock data
    mock_comparison = [
        {"agent_id": 1, "tasks_completed": 100, "avg_rating": 4.5, "success_rate": 0.92},
        {"agent_id": 2, "tasks_completed": 150, "avg_rating": 4.2, "success_rate": 0.88},
        {"agent_id": 3, "tasks_completed": 80, "avg_rating": 4.8, "success_rate": 0.95},
    ]
    return mock_comparison