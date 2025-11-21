from enum import Enum


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


class TemplateStatus(str, Enum):
    """Possible template statuses"""
    DRAFT = "draft"
    RELEASED = "released"
    DEPRECATED = "deprecated"