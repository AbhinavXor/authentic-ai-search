"""
=========================================================
MODULE: Source Content Scorer

Project:
Authentic AI Search

Engine:
VRA Search Engine

Purpose:
Build unified source score from all evidence signals.

Author:
Abhinav

Version:
1.0.0
=========================================================
"""

from typing import Any, Dict, List


class SourceContentScorer:
    """
    Unified source scoring engine.
    """

    def __init__(self) -> None:
        pass

    def score_record(
        self,
        record: Dict[str, Any]
    ) -> float:
        """
        Calculate unified source score.
        """

        authority_score = float(
            record.get(
                "authority_score",
                0
            )
        )

        reputation_score = float(
            record.get(
                "reputation_score",
                0
            )
        )

        reliability_score = float(
            record.get(
                "source_reliability_score",
                0
            )
        )

        freshness_score = float(
            record.get(
                "freshness_score",
                0
            )
        )

        content_quality_score = float(
            record.get(
                "content_quality_score",
                0
            )
        )

        claim_confidence_score = float(
            record.get(
                "claim_confidence_score",
                0
            )
        )

        feedback_score = float(
            record.get(
                "feedback_score",
                50
            )
        )

        unified_score = (
            authority_score * 0.20
            + reputation_score * 0.15
            + reliability_score * 0.15
            + freshness_score * 0.10
            + content_quality_score * 0.15
            + claim_confidence_score * 0.15
            + feedback_score * 0.10
        )

        return round(
            unified_score,
            2
        )

    def enrich_records(
        self,
        evidence_records: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """
        Add unified score.
        """

        updated_records = []

        for record in evidence_records:

            score = self.score_record(
                record
            )

            record[
                "source_content_score"
            ] = score

            if score >= 90:
                level = "elite"

            elif score >= 80:
                level = "excellent"

            elif score >= 70:
                level = "high"

            elif score >= 55:
                level = "medium"

            elif score >= 40:
                level = "low"

            else:
                level = "very_low"

            record[
                "source_content_level"
            ] = level

            updated_records.append(
                record
            )

        return updated_records