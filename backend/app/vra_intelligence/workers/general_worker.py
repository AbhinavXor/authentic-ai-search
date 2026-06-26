"""
=========================================================
MODULE: General Worker

Project:
Authentic AI Search

Engine:
VRA Intelligence

Purpose:
General fallback worker for safe basic answers.

Author:
Abhinav

Version:
2.0.0
=========================================================
"""

from typing import Any
from typing import Dict

from backend.app.vra_intelligence.workers.base_worker import (
    BaseWorker
)


class GeneralWorker(BaseWorker):
    """
    General fallback worker.

    This worker does not hallucinate. It uses available
    context first and returns safe fallback messages.
    """

    @property
    def worker_name(self) -> str:
        return "general_worker"

    def execute(
        self,
        context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Execute general fallback response.
        """

        query = context.get("query", "")
        answer = context.get("answer", "")
        vra_result = context.get("vra_result")

        if answer:
            final_answer = answer

        elif isinstance(vra_result, dict) and vra_result.get("answer"):
            final_answer = vra_result.get("answer", "")

        else:
            final_answer = (
                "I could not generate a fully verified answer from the "
                "available evidence yet. Please try asking the question "
                "with more detail."
            )

        return {
            "worker": self.worker_name,
            "status": "completed",
            "query": query,
            "answer": final_answer,
            "fallback_used": True
        }