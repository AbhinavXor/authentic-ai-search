"""
=========================================================
MODULE: Document Worker

Project:
Authentic AI Search

Engine:
VRA Intelligence

Purpose:
Plan DOCX/document artifact generation from VRA
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


class DocumentWorker(BaseWorker):
    """
    Document worker.

    MVP:
    - Detects document/DOCX request.
    - Builds document generation plan.
    - Future: connect python-docx artifact builder.
    """

    @property
    def worker_name(self) -> str:
        return "document_worker"

    def _select_document_style(
        self,
        query: str
    ) -> str:
        query_lower = query.lower()

        if "proposal" in query_lower:
            return "proposal"

        if "professional" in query_lower:
            return "professional"

        if "academic" in query_lower:
            return "academic"

        if "corporate" in query_lower:
            return "corporate"

        if "simple" in query_lower:
            return "simple"

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

        document_style = self._select_document_style(
            query
        )

        return {
            "worker": self.worker_name,
            "status": "completed",
            "query": query,
            "answer": (
                "A document can be generated for this request. "
                "The document worker has prepared a DOCX plan."
            ),
            "document_required": True,
            "document_style": document_style,
            "document_plan": {
                "title": "Authentic AI Verified Document",
                "style": document_style,
                "sections": [
                    "Title",
                    "Summary",
                    "Verified Answer",
                    "Key Points",
                    "Evidence",
                    "Sources",
                    "Verification Notes"
                ],
                "include_citations": True,
                "include_evidence": True
            },
            "source_count": len(citations),
            "evidence_count": len(evidence_records),
            "base_answer": answer
        }