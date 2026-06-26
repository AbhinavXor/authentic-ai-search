"""
=========================================================
MODULE: Ollama Provider

Project:
Authentic AI Search

Engine:
VRA Intelligence

Purpose:
Execute local LLM requests using Ollama.

Author:
Abhinav

Version:
1.0.0
=========================================================
"""

import requests

from typing import Dict
from typing import Any


class OllamaProvider:

    def __init__(
        self,
        base_url: str = "http://localhost:11434"
    ) -> None:

        self.base_url = base_url

    def generate(
        self,
        model_name: str,
        prompt: str,
        system_prompt: str = ""
    ) -> Dict[str, Any]:

        try:

            response = requests.post(

                f"{self.base_url}/api/generate",

                json={
                    "model": model_name,
                    "prompt": prompt,
                    "system": system_prompt,
                    "stream": False
                },

                timeout=120
            )

            response.raise_for_status()

            data = response.json()

            return {
                "status": "success",
                "provider": "ollama",
                "model": model_name,
                "response": data.get(
                    "response",
                    ""
                )
            }

        except Exception as e:

            return {
                "status": "failed",
                "provider": "ollama",
                "model": model_name,
                "error": str(e)
            }