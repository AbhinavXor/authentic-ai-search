"""
=========================================================
MODULE: Search Worker

Project:
Authentic AI Search

Engine:
VRA Intelligence

Purpose:
Execute VRA Search Engine queries.

Author:
Abhinav

Version:
1.1.0
=========================================================
"""

from typing import Any, Dict

from backend.app.vra.pipeline import VRAPipeline
from backend.app.vra.types import UserQuery
from backend.app.vra_intelligence.workers.base_worker import (
    BaseWorker
)


class SearchWorker(BaseWorker):
    """
    Search execution worker.

    This worker uses the current VRA pipeline without
    changing pipeline.py.
    """

    def __init__(self) -> None:
        self.pipeline = VRAPipeline()

    @property
    def worker_name(self) -> str:
        return "search_worker"

    def execute(
        self,
        context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Execute VRA search.
        """

        query = context.get("query", "")

        if not query:
            return {
                "worker": self.worker_name,
                "status": "failed",
                "error": "Query is missing."
            }

        try:
            user_query = UserQuery(
                query_text=query
            )

            result = self.pipeline.process_query(
                user_query
            )

            return {
                "worker": self.worker_name,
                "status": "completed",
                "query": query,
                "answer": result.answer,
                "trust_score": result.trust_score,
                "confidence_score": result.confidence_score,
                "verification_status": result.verification_status,
                "verification_badge": result.verification_badge,
                "sources": [
                    {
                        "title": source.title,
                        "url": source.url,
                        "domain": source.domain,
                        "source_type": source.source_type,
                        "authority_score": source.authority_score,
                        "freshness_score": source.freshness_score
                    }
                    for source in result.sources
                ],
                "evidence_records": result.evidence_records,
                "evidence_summary": result.evidence_summary,
                "citations": result.citations,
                "warning_message": result.warning_message
            }

        except Exception as error:
            return {
                "worker": self.worker_name,
                "status": "failed",
                "query": query,
                "error": str(error)
            }