"""
=========================================================
MODULE: Model Router

Project:
Authentic AI Search

Engine:
VRA Intelligence

Purpose:
Select best model route for a task.

Author:
Abhinav

Version:
1.0.0
=========================================================
"""

from typing import Any, Dict


class ModelRouter:
    """
    Select model strategy.

    Priority:
    1. Code / VRA
    2. Local LLM
    3. API fallback layer
    """

    def route(
        self,
        task_type: str,
        complexity_level: str
    ) -> Dict[str, Any]:

        route = {
            "primary_layer": "code_vra",
            "secondary_layer": "local_llm",
            "api_fallback_enabled": True,
            "recommended_local_model": "qwen",
            "api_chain": [
                "gemini",
                "claude",
                "openai"
            ]
        }

        if task_type in {
            "math_science",
            "reasoning"
        }:
            route["recommended_local_model"] = "deepseek_r1"
            route["api_chain"] = [
                "deepseek",
                "gemini",
                "openai"
            ]

        elif task_type == "coding":
            route["recommended_local_model"] = "qwen_coder"
            route["api_chain"] = [
                "claude",
                "openai",
                "deepseek"
            ]

        elif task_type == "image_analysis":
            route["recommended_local_model"] = "llava"
            route["api_chain"] = [
                "gemini_vision",
                "openai_vision",
                "claude_vision"
            ]

        elif task_type == "research":
            route["recommended_local_model"] = "qwen"
            route["api_chain"] = [
                "gemini_pro",
                "claude",
                "openai"
            ]

        if complexity_level in {
            "complex",
            "expert"
        }:
            route["primary_layer"] = "local_llm"
            route["secondary_layer"] = "api_fallback"

        return route