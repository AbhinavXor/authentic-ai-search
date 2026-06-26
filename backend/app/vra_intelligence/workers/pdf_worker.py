"""
=========================================================
MODULE: PDF Worker

Project:
Authentic AI Search

Engine:
VRA Intelligence

Purpose:
Plan PDF artifact generation from VRA verified answer.

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


class PDFWorker(BaseWorker):
    """
    PDF worker.

    MVP:
    - Detects PDF/report request.
    - Builds PDF generation plan.
    - Future: connect artifact PDF builder.
    """

    @property
    def worker_name(self) -> str:
        return "pdf_worker"

    def _select_pdf_style(
        self,
        query: str
    ) -> str:
        query_lower = query.lower()

        if "professional" in query_lower:
            return "professional"

        if "academic" in query_lower:
            return "academic"

        if "corporate" in query_lower:
            return "corporate"

        if "executive" in query_lower:
            return "executive"

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

        pdf_style = self._select_pdf_style(query)

        return {
            "worker": self.worker_name,
            "status": "completed",
            "query": query,
            "answer": (
                "A PDF artifact can be generated for this request. "
                "The PDF worker has prepared a document plan."
            ),
            "pdf_required": True,
            "pdf_style": pdf_style,
            "pdf_plan": {
                "title": "Authentic AI Verified Report",
                "style": pdf_style,
                "sections": [
                    "Executive Summary",
                    "Verified Answer",
                    "Key Evidence",
                    "Sources",
                    "Trust & Verification Notes"
                ],
                "include_citations": True,
                "include_evidence": True,
                "include_charts_if_available": True
            },
            "source_count": len(citations),
            "evidence_count": len(evidence_records),
            "base_answer": answer
        }