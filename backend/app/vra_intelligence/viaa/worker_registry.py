"""
=========================================================
MODULE: VIAA Worker Registry

Project:
Authentic AI Search

Engine:
VRA Intelligence Allocation Algorithm (VIAA)

Purpose:
Maintain available worker definitions.

Author:
Abhinav

Version:
1.0.0
=========================================================
"""

from typing import Any, Dict


class WorkerRegistry:
    """
    Registry of all available workers.

    Future:
    - Dynamic worker loading
    - Local LLM workers
    - API workers
    - Agent workers
    """

    def __init__(self) -> None:

        self.workers = {

            "search_worker": {
                "enabled": True,
                "category": "search"
            },

            "research_worker": {
                "enabled": True,
                "category": "research"
            },

            "reasoning_worker": {
                "enabled": True,
                "category": "reasoning"
            },

            "verification_worker": {
                "enabled": True,
                "category": "verification"
            },

            "pdf_worker": {
                "enabled": True,
                "category": "document"
            },

            "ppt_worker": {
                "enabled": True,
                "category": "presentation"
            },

            "document_worker": {
                "enabled": True,
                "category": "document"
            },

            "chart_worker": {
                "enabled": True,
                "category": "visualization"
            },

            "vision_worker": {
                "enabled": True,
                "category": "vision"
            },

            "image_generation_worker": {
                "enabled": True,
                "category": "image_generation"
            },

            "code_worker": {
                "enabled": True,
                "category": "coding"
            },

            "emotional_worker": {
                "enabled": True,
                "category": "emotional"
            },

            "general_worker": {
                "enabled": True,
                "category": "general"
            }
        }

    def get_worker(
        self,
        worker_name: str
    ) -> Dict[str, Any]:

        return self.workers.get(
            worker_name,
            {}
        )

    def worker_exists(
        self,
        worker_name: str
    ) -> bool:

        return worker_name in self.workers

    def get_all_workers(
        self
    ) -> Dict[str, Any]:

        return self.workers