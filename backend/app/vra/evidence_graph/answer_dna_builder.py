"""
=========================================================
MODULE: Answer DNA Builder

Project:
Authentic AI Search

Engine:
VRA Search Engine

Purpose:
Build source contribution breakdown for an answer.

Author:
Abhinav

Version:
1.0.0
=========================================================
"""

from typing import Any, Dict, List


class AnswerDNABuilder:
    """
    Builds Answer DNA.

    Answer DNA explains how much each verified source
    contributed to the final answer.
    """

    def __init__(self) -> None:
        pass

    def _source_weight(
        self,
        record: Dict[str, Any]
    ) -> float:
        """
        Calculate source contribution weight.
        """

        if record.get("retrieval_status") != "success":
            return 0.0

        authority_score = float(
            record.get("authority_score", 0)
        )

        reputation_score = float(
            record.get("reputation_score", 0)
        )

        reliability_score = float(
            record.get("source_reliability_score", 0)
        )

        freshness_score = float(
            record.get("freshness_score", 0)
        )

        claim_bonus = (
            10.0
            if record.get("extracted_claim")
            else 0.0
        )

        weight = (
            authority_score * 0.30
            + reputation_score * 0.30
            + reliability_score * 0.25
            + freshness_score * 0.10
            + claim_bonus * 0.05
        )

        return round(weight, 4)

    def build(
        self,
        evidence_records: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """
        Build source contribution percentages.
        """

        weighted_sources = []

        for record in evidence_records:
            weight = self._source_weight(record)

            if weight <= 0:
                continue

            weighted_sources.append(
                {
                    "source": record.get("source_name"),
                    "domain": record.get("domain"),
                    "url": record.get("source_url"),
                    "claim": record.get("extracted_claim"),
                    "raw_weight": weight
                }
            )

        total_weight = sum(
            item["raw_weight"]
            for item in weighted_sources
        )

        if total_weight <= 0:
            return []

        answer_dna = []

        for item in weighted_sources:
            contribution = (
                item["raw_weight"] / total_weight
            ) * 100

            answer_dna.append(
                {
                    "source": item.get("source"),
                    "domain": item.get("domain"),
                    "url": item.get("url"),
                    "claim": item.get("claim"),
                    "contribution_percent": round(
                        contribution,
                        2
                    )
                }
            )

        answer_dna.sort(
            key=lambda item: item["contribution_percent"],
            reverse=True
        )

        return answer_dna