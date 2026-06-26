"""
=========================================================
MODULE: Task Decomposer

Project:
Authentic AI Search

Engine:
VRA Intelligence

Purpose:
Break complex user requests into smaller executable tasks.

Author:
Abhinav

Version:
1.0.0
=========================================================
"""

from typing import Any, Dict, List


class TaskDecomposer:
    """
    Decompose complex tasks into steps.
    """

    def decompose(
        self,
        query: str
    ) -> Dict[str, Any]:

        query_lower = query.lower()

        steps: List[Dict[str, Any]] = []

        if "research" in query_lower or "report" in query_lower:
            steps.append(
                {
                    "step": 1,
                    "task": "collect_verified_sources",
                    "worker": "research_worker"
                }
            )

            steps.append(
                {
                    "step": 2,
                    "task": "verify_evidence",
                    "worker": "verification_worker"
                }
            )

            steps.append(
                {
                    "step": 3,
                    "task": "compose_research_answer",
                    "worker": "research_worker"
                }
            )

        if "pdf" in query_lower:
            steps.append(
                {
                    "step": len(steps) + 1,
                    "task": "build_pdf_artifact",
                    "worker": "pdf_worker"
                }
            )

        if "ppt" in query_lower or "presentation" in query_lower:
            steps.append(
                {
                    "step": len(steps) + 1,
                    "task": "build_ppt_artifact",
                    "worker": "ppt_worker"
                }
            )

        if "chart" in query_lower or "graph" in query_lower:
            steps.append(
                {
                    "step": len(steps) + 1,
                    "task": "build_visual_chart",
                    "worker": "chart_worker"
                }
            )

        if not steps:
            steps.append(
                {
                    "step": 1,
                    "task": "answer_user_query",
                    "worker": "general_worker"
                }
            )

        return {
            "query": query,
            "decomposed_steps": steps,
            "step_count": len(steps)
        }