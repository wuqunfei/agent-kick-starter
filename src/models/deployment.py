from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


class DeploymentStatus(str, Enum):
    """Possible deployment statuses"""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    SUCCESS = "success"
    FAILED = "failed"
    CANCELLED = "cancelled"
    RETRYING = "retrying"
    UPDATING = "updating"
    DELETING = "deleting"
    DELETED = "deleted"


class DeploymentManifest(BaseModel):
    """
    A file that defines all the cloud resources required for the agent 
    and instructions for deployment
    """
    id: str = Field(..., description="Unique identifier for the deployment")
    template_id: str = Field(..., description="Reference to the template being deployed")
    profile_id: str = Field(..., description="Reference to the configuration profile being used")
    cloud_provider: str = Field(..., description="Cloud platform where agent is deployed")
    resources: List[Dict[str, Any]] = Field(default_factory=list, description="List of cloud resources to provision")
    deployment_path: str = Field(..., description="Path where agent is deployed")
    status: DeploymentStatus = Field(..., description="Current status of the deployment")
    created_at: datetime = Field(default_factory=datetime.now, description="Timestamp when deployment was initiated")
    updated_at: datetime = Field(default_factory=datetime.now, description="Timestamp when deployment was last updated")
    deployment_logs: Optional[str] = Field(None, description="Reference to deployment logs")