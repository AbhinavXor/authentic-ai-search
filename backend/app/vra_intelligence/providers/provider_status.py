"""
=========================================================
MODULE: Provider Status
=========================================================
"""

from typing import Dict, Any


class ProviderStatus:

    def get_status(
        self,
        provider_name: str
    ) -> Dict[str, Any]:

        return {
            "provider": provider_name,
            "available": True,
            "healthy": True,
            "latency_ms": 0
        }