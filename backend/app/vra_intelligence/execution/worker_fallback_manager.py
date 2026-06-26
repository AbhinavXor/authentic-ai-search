"""
=========================================================
MODULE: Worker Fallback Manager

Project:
Authentic AI Search

Engine:
VRA Intelligence

Purpose:
Provide fallback workers when primary workers fail.

Author:
Abhinav

Version:
2.0.0
=========================================================
"""

from typing import Dict
from typing import List


class WorkerFallbackManager:
    """
    Manages fallback worker selection.
    """

    def __init__(self) -> None:
        self.fallback_map = {
            "research_worker": [
                "search_worker",
                "general_worker"
            ],
            "reasoning_worker": [
                "general_worker"
            ],
            "verification_worker": [
                "search_worker"
            ],
            "vision_worker": [
                "general_worker"
            ],
            "image_generation_worker": [
                "general_worker"
            ],
            "pdf_worker": [
                "document_worker",
                "general_worker"
            ],
            "ppt_worker": [
                "document_worker",
                "general_worker"
            ],
            "document_worker": [
                "general_worker"
            ],
            "chart_worker": [
                "general_worker"
            ],
            "code_worker": [
                "general_worker"
            ],
            "emotional_worker": [
                "general_worker"
            ],
            "search_worker": [
                "general_worker"
            ],
            "general_worker": []
        }

    def get_fallback_workers(
        self,
        failed_worker: str
    ) -> List[str]:
        """
        Return fallback workers for failed worker.
        """

        return self.fallback_map.get(
            failed_worker,
            [
                "general_worker"
            ]
        )

    def get_first_fallback(
        self,
        failed_worker: str
    ) -> str | None:
        """
        Return first fallback worker.
        """

        fallback_workers = self.get_fallback_workers(
            failed_worker
        )

        if not fallback_workers:
            return None

        return fallback_workers[0]

    def has_fallback(
        self,
        failed_worker: str
    ) -> bool:
        """
        Check whether worker has fallback.
        """

        return len(
            self.get_fallback_workers(
                failed_worker
            )
        ) > 0