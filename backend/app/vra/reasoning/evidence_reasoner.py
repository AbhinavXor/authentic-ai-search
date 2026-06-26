"""
=========================================================
MODULE: Evidence Reasoner

Project:
Authentic AI Search

Engine:
VRA Intelligence

Purpose:
Reason over verified evidence and identify
the most likely factual conclusion.

Author:
Abhinav

Version:
1.0.0
=========================================================
"""

from typing import Any, Dict, List


class EvidenceReasoner:
    """
    Reason over evidence records.

    Future:
    - Local LLM support
    - Consensus reasoning
    - Multi-hop reasoning
    - VIAA integration
    """

    def __init__(self) -> None:
        pass

    def build_reasoning_summary(
        self,
        evidence_records: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Build reasoning summary.
        """

        successful_records = [
            record
            for record in evidence_records
            if record.get(
                "retrieval_status"
            ) == "success"
        ]

        if not successful_records:
            return {
                "reasoning_status": "no_evidence",
                "reasoning_summary": "",
                "most_supported_claim": None
            }

        ranked_records = sorted(
            successful_records,
            key=lambda record:
            record.get(
                "source_content_score",
                0
            ),
            reverse=True
        )

        best_record = ranked_records[0]

        best_claim = (
            best_record.get(
                "extracted_claim"
            )
        )

        source_name = (
            best_record.get(
                "source_name"
            )
        )

        support_count = sum(
            1
            for record in successful_records
            if record.get(
                "extracted_claim"
            )
        )

        reasoning_summary = (
            f"The strongest supported claim "
            f"comes from {source_name}. "
            f"{support_count} verified source(s) "
            f"provided supporting evidence."
        )

        return {
            "reasoning_status": "completed",
            "reasoning_summary": reasoning_summary,
            "most_supported_claim": best_claim,
            "support_count": support_count
        }