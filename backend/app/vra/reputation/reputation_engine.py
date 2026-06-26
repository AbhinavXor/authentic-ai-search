"""
=========================================================
MODULE: Source Reputation Engine

Project:
Authentic AI Search

Purpose:
Calculate historical/source reliability reputation.

Author:
Abhinav

Version:
1.2.0
=========================================================
"""

from typing import Any, Dict, List

from backend.app.vra.ml.source_reliability_model import (
    SourceReliabilityModel
)
from backend.app.storage.source_stats_store import (
    SourceStatsStore
)


class ReputationEngine:
    """
    Calculates source reputation and reliability scores.

    Current:
    - Registry authority
    - Retrieval availability
    - Feedback score from SQLite source stats

    Future:
    - Long-term source accuracy
    - Contradiction history
    - Admin trust overrides
    """

    def __init__(self) -> None:
        self.reliability_model = SourceReliabilityModel()
        self.source_stats_store = SourceStatsStore()

    def _get_feedback_score(
        self,
        domain: str
    ) -> float:
        """
        Get feedback score for a source domain.
        """

        if not domain:
            return 50.0

        stats = self.source_stats_store.get_source_stats(
            domain=domain
        )

        if not stats:
            return 50.0

        return float(
            stats.get(
                "feedback_score",
                50.0
            )
        )

    def calculate_source_reputation(
        self,
        record: Dict[str, Any]
    ) -> float:
        """
        Calculate reputation for one source.
        """

        authority_score = float(
            record.get("authority_score", 0)
        )

        retrieval_status = record.get("retrieval_status")

        availability_score = (
            100.0
            if retrieval_status == "success"
            else 0.0
        )

        feedback_score = self._get_feedback_score(
            domain=record.get("domain", "")
        )

        record["feedback_score"] = feedback_score

        reputation_score = (
            authority_score * 0.50
            + availability_score * 0.30
            + feedback_score * 0.20
        )

        return round(reputation_score, 2)

    def calculate_average_reputation(
        self,
        evidence_records: List[Dict[str, Any]]
    ) -> float:
        """
        Calculate average reputation across sources.
        """

        if not evidence_records:
            return 0.0

        scores = [
            self.calculate_source_reputation(record)
            for record in evidence_records
        ]

        return round(
            sum(scores) / len(scores),
            2
        )

    def enrich_records(
        self,
        evidence_records: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """
        Add reputation, feedback, and reliability scores.
        """

        updated_records: List[Dict[str, Any]] = []

        for record in evidence_records:
            reputation_score = self.calculate_source_reputation(
                record
            )

            record["reputation_score"] = reputation_score

            reliability_result = self.reliability_model.evaluate(
                source_record=record
            )

            record["source_reliability_score"] = (
                reliability_result.get(
                    "source_reliability_score",
                    0
                )
            )

            record["source_reliability_level"] = (
                reliability_result.get(
                    "source_reliability_level",
                    "unknown"
                )
            )

            updated_records.append(record)

        return updated_records