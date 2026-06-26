"""
=========================================================
MODULE: Chart Worker

Project:
Authentic AI Search

Engine:
VRA Intelligence

Purpose:
Plan chart/visual output for data-heavy answers.

Author:
Abhinav

Version:
2.0.0
=========================================================
"""

from typing import Any, Dict, List

from backend.app.vra_intelligence.workers.base_worker import (
    BaseWorker
)


class ChartWorker(BaseWorker):
    """
    Chart worker.

    MVP:
    - Detects chart requirement.
    - Builds chart plan.
    - Future: connect chart_builder.py and frontend visual blocks.
    """

    @property
    def worker_name(self) -> str:
        return "chart_worker"

    def _detect_chart_type(
        self,
        query: str
    ) -> str:
        query_lower = query.lower()

        if "pie" in query_lower:
            return "pie_chart"

        if "line" in query_lower or "trend" in query_lower:
            return "line_chart"

        if "scatter" in query_lower:
            return "scatter_chart"

        if "bar" in query_lower or "compare" in query_lower:
            return "bar_chart"

        return "auto_chart"

    def execute(
        self,
        context: Dict[str, Any]
    ) -> Dict[str, Any]:

        query = context.get("query", "")
        evidence_records: List[Dict[str, Any]] = context.get(
            "evidence_records",
            []
        )

        chart_type = self._detect_chart_type(query)

        return {
            "worker": self.worker_name,
            "status": "completed",
            "query": query,
            "answer": (
                "A visual representation may be useful for this query. "
                "The chart worker has prepared a chart plan."
            ),
            "chart_required": True,
            "chart_type": chart_type,
            "data_source": "vra_evidence",
            "evidence_count": len(evidence_records),
            "chart_plan": {
                "chart_type": chart_type,
                "title": "Auto-generated visual insight",
                "description": "Chart should be generated from verified evidence when numeric data is available."
            }
        }