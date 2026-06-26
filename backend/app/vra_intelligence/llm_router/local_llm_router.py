"""
=========================================================
MODULE: Local LLM Router
=========================================================
"""

from typing import Any, Dict


class LocalLLMRouter:
    """
    Route local LLM tasks.
    """

    def select_model(
        self,
        model_key: str
    ) -> Dict[str, Any]:

        models = {
            "qwen": {
                "provider": "ollama",
                "model": "qwen2.5:7b"
            },
            "deepseek_r1": {
                "provider": "ollama",
                "model": "deepseek-r1:7b"
            },
            "qwen_coder": {
                "provider": "ollama",
                "model": "qwen2.5-coder:7b"
            },
            "llava": {
                "provider": "ollama",
                "model": "llava:7b"
            }
        }

        return models.get(
            model_key,
            models["qwen"]
        )