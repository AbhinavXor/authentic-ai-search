"""
=========================================================
MODULE: Reasoning Worker

Project:
Authentic AI Search

Engine:
VRA Intelligence

Purpose:
Execute lightweight reasoning workflows using VRA evidence.

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


class ReasoningWorker(BaseWorker):
    """
    Reasoning worker.

    MVP:
    - Uses verified evidence.
    - Does not invent facts.
    - Builds simple reasoning summary.
    """

    @property
    def worker_name(self) -> str:
        return "reasoning_worker"

    def _get_verified_claims(
        self,
        evidence_records: List[Dict[str, Any]]
    ) -> List[str]:
        claims = []

        for record in evidence_records:
            if record.get("retrieval_status") != "success":
                continue

            claim = record.get("extracted_claim")

            if claim:
                claims.append(claim)

        return claims

    def execute(
        self,
        context: Dict[str, Any]
    ) -> Dict[str, Any]:

        query = context.get("query", "")
        evidence_records = context.get("evidence_records", [])

        claims = self._get_verified_claims(
            evidence_records
        )

        if claims:
            reasoning_summary = (
                "The answer is supported by verified evidence. "
                f"{len(claims)} claim(s) were found from reachable trusted source(s)."
            )

            answer = claims[0]

        else:
            reasoning_summary = (
                "No verified claim was available for reasoning."
            )

            answer = context.get(
                "answer",
                ""
            )

        return {
            "worker": self.worker_name,
            "status": "completed",
            "query": query,
            "answer": answer,
            "reasoning_summary": reasoning_summary,
            "verified_claims": claims,
            "claim_count": len(claims)
        }