"""KMB API client package.

This wraps the Hong Kong KMB open data endpoints and exposes typed Pydantic models.
"""

from .kmb_eta_client import KmbEtaClient

__all__ = ["KmbEtaClient"]
