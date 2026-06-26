"""
=========================================================
MODULE: Provider Health Monitor
=========================================================
"""

from typing import Dict


class ProviderHealthMonitor:
    """
    Track provider health.

    MVP:
    All providers assumed available.
    Later:
    Track timeout, rate limit, token errors.
    """

    def is_available(
        self,
        provider_name: str
    ) -> bool:

        return True

    def filter_available(
        self,
        providers: list[str]
    ) -> list[str]:

        return [
            provider
            for provider in providers
            if self.is_available(provider)
        ]