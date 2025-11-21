from datetime import datetime
from enum import Enum
from typing import Dict, List, Optional
from pydantic import BaseModel, Field


class AgentFramework(str, Enum):
    """Supported agent frameworks"""
    MICROSOFT = "microsoft"
    AMAZON = "amazon"
    GOOGLE = "google"
    PYDANTIC = "pydantic"


class CloudProvider(str, Enum):
    """Supported cloud providers"""
    AWS = "aws"
    AZURE = "azure"
    GCP = "gcp"


class GenAiAgentTemplate(BaseModel):
    """
    A standardized project structure with all necessary code, configuration, 
    and deployment scripts for a specific agent framework and cloud platform
    """
    id: str = Field(..., description="Unique identifier for the template")
    name: str = Field(..., description="Display name for the template")
    description: str = Field(..., description="Detailed description of the template's purpose")
    framework: AgentFramework = Field(..., description="Agent framework (Microsoft, Amazon, Google, Pydantic)")
    cloud_provider: CloudProvider = Field(..., description="Cloud platform (AWS, Azure, GCP)")
    version: str = Field(..., description="Template version following semantic versioning", 
                        pattern=r"^\d+\.\d+\.\d+(-[a-zA-Z0-9]+)?$")
    path: str = Field(..., description="File system path to template files")
    parameters: List[Dict[str, str]] = Field(default_factory=list, description="List of configurable parameters for the template")
    dependencies: List[str] = Field(default_factory=list, description="Required dependencies and their versions")
    created_at: datetime = Field(default_factory=datetime.now, description="Timestamp when template was created")
    updated_at: datetime = Field(default_factory=datetime.now, description="Timestamp when template was last updated")
    supported_features: List[str] = Field(default_factory=list, description="List of features supported by the template")
    
    class Config:
        use_enum_values = True