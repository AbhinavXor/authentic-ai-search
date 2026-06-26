"""
=========================================================
MODULE: API Fallback Router
=========================================================
"""

from typing import Dict, List


class APIFallbackRouter:
    """
    Build API fallback order.
    """

    def build_chain(
        self,
        api_chain: List[str]
    ) -> Dict[str, List[str]]:

        return {
            "fallback_chain": api_chain,
            "fallback_count": len(api_chain)
        }