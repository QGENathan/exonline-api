#__init__.py
from .client import ExOnlineClient
from .models import AttachmentData, Project, APIResponse, EqItem
from .exceptions import APIError, AuthenticationError

__version__ = "0.1.0"

__all__ = [
    "ExOnlineClient",
    "AttachmentData",
    "Project",
    "APIResponse",
    "APIError",
    "AuthenticationError",
    "EqItem"
]