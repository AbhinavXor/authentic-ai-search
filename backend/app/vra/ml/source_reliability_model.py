"""
=========================================================
MODULE: Source Reliability Model

Project:
Authentic AI Search

Purpose:
Estimate source reliability using feedback and reputation signals.

Author:
Abhinav

Version:
1.0.0
=========================================================
"""

from typing import Any, Dict


class SourceReliabilityModel:
    """
    Rule-based ML placeholder for source reliability.

    Current:
    - Uses authority_score
    - Uses reputation_score
    - Uses feedback_weight

    Future:
    - Train ML model from feedback history
    - Predict source reliability
    - Improve trust score automatically
    """

    def predict(
        self,
        source_record: Dict[str, Any],
        feedback_weight: float = 0.0
    ) -> float:
        """
        Predict source reliability score.
        """

        authority_score = float(
            source_record.get("authority_score", 0)
        )

        reputation_score = float(
            source_record.get(
                "reputation_score",
                authority_score
            )
        )

        feedback_adjustment = feedback_weight * 5.0

        reliability_score = (
            authority_score * 0.40
            + reputation_score * 0.50
            + feedback_adjustment
        )

        return round(
            max(
                0.0,
                min(reliability_score, 100.0)
            ),
            2
        )

    def classify(
        self,
        reliability_score: float
    ) -> str:
        """
        Classify reliability level.
        """

        if reliability_score >= 90:
            return "very_high"

        if reliability_score >= 75:
            return "high"

        if reliability_score >= 50:
            return "medium"

        if reliability_score >= 25:
            return "low"

        return "very_low"

    def evaluate(
        self,
        source_record: Dict[str, Any],
        feedback_weight: float = 0.0
    ) -> Dict[str, Any]:
        """
        Return reliability score and label.
        """

        score = self.predict(
            source_record=source_record,
            feedback_weight=feedback_weight
        )

        return {
            "source": source_record.get("source_name"),
            "domain": source_record.get("domain"),
            "source_reliability_score": score,
            "source_reliability_level": self.classify(score)
        }