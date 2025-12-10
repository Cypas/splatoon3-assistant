# Splatoon3 Assistant - NSO API Module
"""
This module provides:
- NSOAuth: Nintendo Switch Online OAuth authentication
- SplatNet3API: SplatNet3 GraphQL API wrapper
"""

from .nso_auth import NSOAuth
from .splatnet3_api import SplatNet3API

__all__ = ["NSOAuth", "SplatNet3API"]
__version__ = "0.1.1"
