from datetime import datetime
from typing import Any, Dict, Optional
from pydantic import BaseModel, Field


class EvaluationMetrics(BaseModel):
    """
    Standardized data points collected to assess the performance, 
    quality, and effectiveness of the GenAI agent
    """
    id: str = Field(..., description="Unique identifier for the metrics collection")
    deployment_id: str = Field(..., description="Reference to the deployment being evaluated")
    timestamp: datetime = Field(default_factory=datetime.now, description="When the metrics were collected")
    latency: Optional[float] = Field(None, description="Response time metrics in seconds")
    throughput: Optional[float] = Field(None, description="Requests per unit time")
    accuracy: Optional[float] = Field(None, description="Accuracy of agent responses as percentage")
    error_rate: Optional[float] = Field(None, description="Error rate metrics as percentage")
    user_satisfaction: Optional[float] = Field(None, description="User satisfaction scores")
    resource_utilization: Optional[Dict[str, float]] = Field(default_factory=dict, description="Cloud resource usage metrics")
    custom_metrics: Optional[Dict[str, Any]] = Field(default_factory=dict, description="Additional custom metrics defined by user")