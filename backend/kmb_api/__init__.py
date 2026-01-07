"""KMB API client package.

This wraps the Hong Kong KMB open data endpoints and exposes typed Pydantic models.
"""

from .kmb_api import KmbApi

__all__ = ["KmbApi"]
