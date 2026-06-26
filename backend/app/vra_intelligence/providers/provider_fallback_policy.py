"""
=========================================================
MODULE: Provider Fallback Policy
=========================================================
"""

from typing import Dict, List


class ProviderFallbackPolicy:

    def build_chain(
        self,
        task_type: str
    ) -> Dict[str, List[str]]:

        chains = {

            "research": [
                "gemini",
                "claude",
                "openai"
            ],

            "coding": [
                "claude",
                "openai",
                "deepseek"
            ],

            "image_analysis": [
                "gemini",
                "openai",
                "claude"
            ],

            "image_generation": [
                "openai",
                "grok"
            ],

            "general": [
                "gemini",
                "claude",
                "openai"
            ]
        }

        return {
            "fallback_chain":
            chains.get(
                task_type,
                chains["general"]
            )
        }