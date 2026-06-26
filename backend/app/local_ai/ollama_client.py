"""
=========================================================
MODULE: Ollama Client

Project:
Authentic AI Search

Purpose:
Client for local Ollama models.

Author:
Abhinav

Version:
1.0.0
=========================================================
"""

from typing import Any, Dict

import requests


class OllamaClient:
    """
    Lightweight Ollama client.
    """

    def __init__(
        self,
        base_url: str = "http://localhost:11434"
    ) -> None:
        self.base_url = base_url.rstrip("/")

    def generate(
        self,
        model: str,
        prompt: str,
        temperature: float = 0.2
    ) -> Dict[str, Any]:
        """
        Generate response from local model.
        """

        try:
            response = requests.post(
                f"{self.base_url}/api/generate",
                json={
                    "model": model,
                    "prompt": prompt,
                    "stream": False,
                    "options": {
                        "temperature": temperature
                    }
                },
                timeout=60
            )

            if response.status_code != 200:
                return {
                    "status": "failed",
                    "text": "",
                    "error": f"HTTP {response.status_code}"
                }

            data = response.json()

            return {
                "status": "success",
                "text": data.get("response", "").strip(),
                "error": None
            }

        except Exception as error:
            return {
                "status": "failed",
                "text": "",
                "error": str(error)
            }