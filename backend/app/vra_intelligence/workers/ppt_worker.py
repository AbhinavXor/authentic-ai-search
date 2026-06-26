"""
=========================================================
MODULE: PPT Worker

Project:
Authentic AI Search

Engine:
VRA Intelligence

Purpose:
Plan PPT/presentation artifact generation from VRA
verified answer and evidence.

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


class PPTWorker(BaseWorker):
    """
    PPT worker.

    MVP:
    - Detects presentation/slides request.
    - Builds PPT generation plan.
    - Future: connect python-pptx artifact builder.
    """

    @property
    def worker_name(self) -> str:
        return "ppt_worker"

    def _select_ppt_style(
        self,
        query: str
    ) -> str:
        query_lower = query.lower()

        if "pitch" in query_lower or "startup" in query_lower:
            return "pitch_deck"

        if "professional" in query_lower:
            return "professional"

        if "corporate" in query_lower:
            return "corporate"

        if "academic" in query_lower or "research" in query_lower:
            return "academic"

        if "simple" in query_lower:
            return "simple"

        if "colorful" in query_lower:
            return "colorful"

        return "standard"

    def execute(
        self,
        context: Dict[str, Any]
    ) -> Dict[str, Any]:

        query = context.get("query", "")
        answer = context.get("answer", "")
        citations: List[Dict[str, Any]] = context.get(
            "citations",
            []
        )
        evidence_records: List[Dict[str, Any]] = context.get(
            "evidence_records",
            []
        )

        ppt_style = self._select_ppt_style(query)

        return {
            "worker": self.worker_name,
            "status": "completed",
            "query": query,
            "answer": (
                "A presentation can be generated for this request. "
                "The PPT worker has prepared a slide deck plan."
            ),
            "ppt_required": True,
            "ppt_style": ppt_style,
            "ppt_plan": {
                "title": "Authentic AI Verified Presentation",
                "style": ppt_style,
                "slides": [
                    "Title Slide",
                    "Executive Summary",
                    "Key Findings",
                    "Evidence & Sources",
                    "Visual Insights",
                    "Verification Notes",
                    "Conclusion"
                ],
                "include_citations": True,
                "include_charts_if_available": True,
                "include_source_slide": True
            },
            "source_count": len(citations),
            "evidence_count": len(evidence_records),
            "base_answer": answer
        }