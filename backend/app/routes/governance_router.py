from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import List, Optional
from enum import Enum
from datetime import datetime

router = APIRouter(prefix="/governance", tags=["governance"])

class BoundaryType(str, Enum):
    ETHICAL = "Ethical"
    LEGAL = "Legal"
    OPERATIONAL = "Operational"
    FINANCIAL = "Financial"
    REPUTATIONAL = "Reputational"

class BoundaryStatus(str, Enum):
    ACTIVE = "Active"
    WARNING = "Warning"
    VIOLATED = "Violated"

class BoundaryBase(BaseModel):
    name: str
    boundary_type: BoundaryType
    description: str

class BoundaryCreate(BoundaryBase):
    pass

class Boundary(BoundaryBase):
    id: int
    status: BoundaryStatus
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

class FeedbackType(str, Enum):
    APPROVAL = "Approval"
    REJECTION = "Rejection"
    MODIFICATION = "Modification"
    CLARIFICATION = "Clarification"

class FeedbackBase(BaseModel):
    agent_id: int
    task: str
    feedback_type: FeedbackType
    feedback_details: str

class FeedbackCreate(FeedbackBase):
    pass

class Feedback(FeedbackBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True

class ReviewStatus(str, Enum):
    PENDING = "Pending"
    APPROVED = "Approved"
    REJECTED = "Rejected"

class ReviewBase(BaseModel):
    output_type: str
    output_name: str
    agent_id: int
    review_status: ReviewStatus

class ReviewCreate(ReviewBase):
    pass

class Review(ReviewBase):
    id: int
    review_date: datetime

    class Config:
        orm_mode = True

class AlertType(str, Enum):
    BOUNDARY_VIOLATION = "Boundary Violation"
    ANOMALOUS_BEHAVIOR = "Anomalous Behavior"
    SYSTEM_ERROR = "System Error"
    HUMAN_FEEDBACK_REQUIRED = "Human Feedback Required"

class AlertUrgency(str, Enum):
    LOW = "Low"
    MEDIUM = "Medium"
    HIGH = "High"
    CRITICAL = "Critical"

class AlertStatus(str, Enum):
    UNRESOLVED = "Unresolved"
    UNDER_INVESTIGATION = "Under Investigation"
    RESOLVED = "Resolved"
    PENDING = "Pending"

class AlertBase(BaseModel):
    alert_type: AlertType
    description: str
    urgency: AlertUrgency

class AlertCreate(AlertBase):
    pass

class Alert(AlertBase):
    id: int
    status: AlertStatus
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

# Mock databases
boundaries_db = []
feedbacks_db = []
reviews_db = []
alerts_db = []

@router.get("/boundaries", response_model=List[Boundary])
async def list_boundaries():
    return boundaries_db

@router.post("/boundaries", response_model=Boundary, status_code=201)
async def create_boundary(boundary: BoundaryCreate):
    new_boundary = Boundary(
        id=len(boundaries_db) + 1,
        **boundary.dict(),
        status=BoundaryStatus.ACTIVE,
        created_at=datetime.now(),
        updated_at=datetime.now()
    )
    boundaries_db.append(new_boundary)
    return new_boundary

@router.get("/boundaries/{boundary_id}", response_model=Boundary)
async def get_boundary(boundary_id: int):
    boundary = next((b for b in boundaries_db if b.id == boundary_id), None)
    if boundary is None:
        raise HTTPException(status_code=404, detail="Boundary not found")
    return boundary

@router.put("/boundaries/{boundary_id}", response_model=Boundary)
async def update_boundary(boundary_id: int, boundary_update: BoundaryBase):
    boundary = next((b for b in boundaries_db if b.id == boundary_id), None)
    if boundary is None:
        raise HTTPException(status_code=404, detail="Boundary not found")
    
    for key, value in boundary_update.dict().items():
        setattr(boundary, key, value)
    
    boundary.updated_at = datetime.now()
    return boundary

@router.post("/feedback", response_model=Feedback, status_code=201)
async def submit_feedback(feedback: FeedbackCreate):
    new_feedback = Feedback(
        id=len(feedbacks_db) + 1,
        **feedback.dict(),
        created_at=datetime.now()
    )
    feedbacks_db.append(new_feedback)
    return new_feedback

@router.get("/feedback", response_model=List[Feedback])
async def list_feedback(agent_id: Optional[int] = None):
    if agent_id:
        return [f for f in feedbacks_db if f.agent_id == agent_id]
    return feedbacks_db

@router.post("/reviews", response_model=Review, status_code=201)
async def submit_review(review: ReviewCreate):
    new_review = Review(
        id=len(reviews_db) + 1,
        **review.dict(),
        review_date=datetime.now()
    )
    reviews_db.append(new_review)
    return new_review

@router.get("/reviews", response_model=List[Review])
async def list_reviews(agent_id: Optional[int] = None, status: Optional[ReviewStatus] = None):
    filtered_reviews = reviews_db
    if agent_id:
        filtered_reviews = [r for r in filtered_reviews if r.agent_id == agent_id]
    if status:
        filtered_reviews = [r for r in filtered_reviews if r.review_status == status]
    return filtered_reviews

@router.post("/alerts", response_model=Alert, status_code=201)
async def create_alert(alert: AlertCreate):
    new_alert = Alert(
        id=len(alerts_db) + 1,
        **alert.dict(),
        status=AlertStatus.UNRESOLVED,
        created_at=datetime.now(),
        updated_at=datetime.now()
    )
    alerts_db.append(new_alert)
    return new_alert

@router.get("/alerts", response_model=List[Alert])
async def list_alerts(status: Optional[AlertStatus] = None, urgency: Optional[AlertUrgency] = None):
    filtered_alerts = alerts_db
    if status:
        filtered_alerts = [a for a in filtered_alerts if a.status == status]
    if urgency:
        filtered_alerts = [a for a in filtered_alerts if a.urgency == urgency]
    return filtered_alerts

@router.put("/alerts/{alert_id}", response_model=Alert)
async def update_alert_status(alert_id: int, status: AlertStatus):
    alert = next((a for a in alerts_db if a.id == alert_id), None)
    if alert is None:
        raise HTTPException(status_code=404, detail="Alert not found")
    alert.status = status
    alert.updated_at = datetime.now()
    return alert
