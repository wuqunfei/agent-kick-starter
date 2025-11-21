from datetime import datetime
from enum import Enum
from typing import Any, Dict, Optional
from pydantic import BaseModel, Field


class EnvironmentType(str, Enum):
    """Supported environment types"""
    DEVELOPMENT = "development"
    STAGING = "staging"
    PRODUCTION = "production"


class ConfigurationProfile(BaseModel):
    """
    Environment-specific settings that allow customization of the agent 
    without modifying core template files
    """
    id: str = Field(..., description="Unique identifier for the configuration profile")
    name: str = Field(..., description="Display name for the profile")
    template_id: str = Field(..., description="Reference to the associated template")
    environment: EnvironmentType = Field(..., description="Environment type (development, staging, production)")
    parameters: Dict[str, Any] = Field(default_factory=dict, description="Dictionary of parameter values for this profile")
    cloud_credentials: Optional[Dict[str, str]] = Field(None, description="Cloud provider-specific credentials")
    overrides: Optional[Dict[str, Any]] = Field(default_factory=dict, description="Additional configuration overrides")
    created_at: datetime = Field(default_factory=datetime.now, description="Timestamp when profile was created")
    updated_at: datetime = Field(default_factory=datetime.now, description="Timestamp when profile was last updated")