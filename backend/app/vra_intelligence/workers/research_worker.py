"""
=========================================================
MODULE: Research Worker

Project:
Authentic AI Search

Engine:
VRA Intelligence

Purpose:
Execute deep research workflows using
verified VRA evidence.

Author:
Abhinav

Version:
2.0.0
=========================================================
"""

from typing import Any
from typing import Dict
from typing import List

from backend.app.vra.pipeline import VRAPipeline
from backend.app.vra.types import UserQuery

from backend.app.vra_intelligence.workers.base_worker import (
    BaseWorker
)


class ResearchWorker(
    BaseWorker
):
    """
    Deep research worker.

    Uses:
    - VRA Search
    - Verification
    - Evidence synthesis

    Future:
    - Multi-source research
    - Academic mode
    - Long report generation
    - Agent integration
    """

    def __init__(self) -> None:

        self.pipeline = VRAPipeline()

    @property
    def worker_name(
        self
    ) -> str:

        return "research_worker"

    def _extract_key_findings(
        self,
        evidence_records: List[Dict[str, Any]]
    ) -> List[str]:

        findings = []

        for record in evidence_records:

            claim = record.get(
                "extracted_claim"
            )

            if claim:
                findings.append(
                    claim
                )

        return findings[:10]

    def execute(
        self,
        context: Dict[str, Any]
    ) -> Dict[str, Any]:

        query = context.get(
            "query",
            ""
        )

        if not query:

            return {
                "worker": self.worker_name,
                "status": "failed",
                "error": "Query missing"
            }

        try:

            user_query = UserQuery(
                query_text=query
            )

            result = (
                self.pipeline.process_query(
                    user_query
                )
            )

            findings = (
                self._extract_key_findings(
                    result.evidence_records
                )
            )

            return {

                "worker":
                self.worker_name,

                "status":
                "completed",

                "query":
                query,

                "research_answer":
                result.answer,

                "key_findings":
                findings,

                "trust_score":
                result.trust_score,

                "confidence_score":
                result.confidence_score,

                "verification_status":
                result.verification_status,

                "verification_badge":
                result.verification_badge,

                "source_count":
                len(result.sources),

                "sources":
                result.sources,

                "evidence_records":
                result.evidence_records,

                "citations":
                result.citations,

                "warning_message":
                result.warning_message
            }

        except Exception as error:

            return {

                "worker":
                self.worker_name,

                "status":
                "failed",

                "query":
                query,

                "error":
                str(error)
            }