"""
=========================================================
MODULE: Local Model Health

Project:
Authentic AI Search

Purpose:
Check local Ollama model availability.

Author:
Abhinav

Version:
1.0.0
=========================================================
"""

from typing import Any, Dict

import requests


class LocalModelHealth:
    """
    Health checker for local Ollama.
    """

    def __init__(
        self,
        base_url: str = "http://localhost:11434"
    ) -> None:
        self.base_url = base_url.rstrip("/")

    def check(
        self
    ) -> Dict[str, Any]:
        """
        Check Ollama availability.
        """

        try:
            response = requests.get(
                f"{self.base_url}/api/tags",
                timeout=5
            )

            if response.status_code != 200:
                return {
                    "available": False,
                    "models": [],
                    "error": f"HTTP {response.status_code}"
                }

            data = response.json()

            models = [
                item.get("name")
                for item in data.get("models", [])
            ]

            return {
                "available": True,
                "models": models,
                "error": None
            }

        except Exception as error:
            return {
                "available": False,
                "models": [],
                "error": str(error)
            }