from pydantic import BaseModel, Field
from typing import List, Optional
from enum import Enum
from datetime import datetime

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

class Boundary(BaseModel):
    name: str
    boundary_type: BoundaryType
    description: str
    status: BoundaryStatus = BoundaryStatus.ACTIVE

class FeedbackType(str, Enum):
    APPROVAL = "Approval"
    REJECTION = "Rejection"
    MODIFICATION = "Modification"
    CLARIFICATION = "Clarification"

class Feedback(BaseModel):
    agent: str
    task: str
    feedback_type: FeedbackType
    feedback_details: str
    timestamp: datetime = Field(default_factory=datetime.now)

class ReviewStatus(str, Enum):
    PENDING = "Pending"
    APPROVED = "Approved"
    REJECTED = "Rejected"

class OutputReview(BaseModel):
    output_type: str
    output_name: str
    agent: str
    review_status: ReviewStatus
    review_date: datetime = Field(default_factory=datetime.now)

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

class Alert(BaseModel):
    alert_type: AlertType
    description: str
    urgency: AlertUrgency
    status: AlertStatus = AlertStatus.UNRESOLVED
    created_at: datetime = Field(default_factory=datetime.now)

class Governance(BaseModel):
    boundaries: List[Boundary]
    feedbacks: List[Feedback]
    output_reviews: List[OutputReview]
    alerts: List[Alert]

# Example usage:
example_governance = Governance(
    boundaries=[
        Boundary(
            name="Company Values Adherence",
            boundary_type=BoundaryType.ETHICAL,
            description="Ensure agents adhere to company values and principles",
            status=BoundaryStatus.ACTIVE
        ),
        Boundary(
            name="Budget Constraints",
            boundary_type=BoundaryType.FINANCIAL,
            description="Stay within allocated budgets and resource limits",
            status=BoundaryStatus.WARNING
        )
    ],
    feedbacks=[
        Feedback(
            agent="Sales AI",
            task="Generated product description",
            feedback_type=FeedbackType.APPROVAL,
            feedback_details="Great job, the description is accurate and compelling"
        )
    ],
    output_reviews=[
        OutputReview(
            output_type="Blog post",
            output_name="Top 10 AI Trends for 2025",
            agent="Marketing Assistant",
            review_status=ReviewStatus.PENDING
        )
    ],
    alerts=[
        Alert(
            alert_type=AlertType.BOUNDARY_VIOLATION,
            description="Sales AI attempted to access restricted data",
            urgency=AlertUrgency.HIGH,
            status=AlertStatus.UNRESOLVED
        )
    ]
)

print(example_governance.json(indent=2))
