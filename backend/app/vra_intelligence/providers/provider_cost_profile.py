"""
=========================================================
MODULE: Provider Cost Profile
=========================================================
"""

from typing import Dict, Any


class ProviderCostProfile:

    def get_cost_profile(
        self,
        provider_name: str
    ) -> Dict[str, Any]:

        return {
            "provider": provider_name,
            "estimated_cost": "unknown",
            "priority": 1
        }