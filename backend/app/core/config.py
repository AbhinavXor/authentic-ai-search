"""
=========================================================
MODULE: Configuration Management

Project:
Authentic AI Search

Engine:
VRA (Verified Resource Algorithm)

Purpose:
Central configuration management for the
entire application.

Responsibilities:
- Environment variables
- Application settings
- Project metadata
- Future database settings
- Future AI settings
- Future VRA settings

Author:
Abhinav

Version:
0.1.0
=========================================================
"""

from dataclasses import dataclass


@dataclass
class ProjectConfig:
    """
    Main project configuration.

    This class contains global project
    information that can be accessed
    throughout the application.
    """

    PROJECT_NAME: str = "Authentic AI Search"

    PROJECT_VERSION: str = "0.1.0"

    PROJECT_AUTHOR: str = "Abhinav"

    DEBUG_MODE: bool = True

    API_PREFIX: str = "/api"

    VRA_ENGINE_NAME: str = "Verified Resource Algorithm"

    VRA_ENGINE_VERSION: str = "0.1.0"


# Global config object
config = ProjectConfig()