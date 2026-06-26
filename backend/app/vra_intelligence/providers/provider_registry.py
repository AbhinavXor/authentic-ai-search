"""
=========================================================
MODULE: Provider Registry

Project:
Authentic AI Search

Purpose:
Central registry for all AI providers.

Author:
Abhinav

Version:
1.0.0
=========================================================
"""

from typing import Dict, Any


class ProviderRegistry:

    def __init__(
        self
    ) -> None:

        self.providers = {

            "gemini": {
                "enabled": True,
                "provider_type": "api"
            },

            "claude": {
                "enabled": True,
                "provider_type": "api"
            },

            "openai": {
                "enabled": True,
                "provider_type": "api"
            },

            "deepseek": {
                "enabled": True,
                "provider_type": "api"
            },

            "grok": {
                "enabled": True,
                "provider_type": "api"
            },

            "qwen_local": {
                "enabled": True,
                "provider_type": "local"
            },

            "deepseek_local": {
                "enabled": True,
                "provider_type": "local"
            },

            "llava_local": {
                "enabled": True,
                "provider_type": "local"
            }
        }

    def get_provider(
        self,
        provider_name: str
    ) -> Dict[str, Any]:

        return self.providers.get(
            provider_name,
            {}
        )

    def get_all(
        self
    ) -> Dict[str, Any]:

        return self.providers