"""
=========================================================
MODULE: Trust Score Engine

Project:
Authentic AI Search

Purpose:
Calculate final VRA trust score from verified evidence.

Version:
2.0.0
=========================================================
"""

from typing import Any, Dict, List


class TrustScoreEngine:
    """
    Calculates trust score using:
    - authority score
    - official/trusted status
    - source authenticity
    - retrieval success
    - relevance/rank score
    - source risk
    """

    def _record_score(
        self,
        record: Dict[str, Any]
    ) -> float:

        if record.get("retrieval_status") != "success":
            return 0.0

        authority_score = float(
            record.get("authority_score", 0) or 0
        )

        relevance_score = float(
            record.get("relevance_score", 0) or 0
        )

        rank_score = float(
            record.get("rank_score", 0) or 0
        )

        official_confidence = float(
            record.get("official_confidence_score", 0) or 0
        )

        score = (
            authority_score * 0.40
            + relevance_score * 0.20
            + rank_score * 0.20
            + official_confidence * 0.20
        )

        if record.get("is_official"):
            score += 8.0

        elif record.get("is_trusted"):
            score += 5.0

        if record.get("can_support_verified_answer") is False:
            score -= 15.0

        risk_level = record.get("source_risk_level")

        risk_penalty = {
            "very_low_risk": 0.0,
            "low_risk": 2.0,
            "medium_risk": 8.0,
            "high_risk": 18.0,
            "very_high_risk": 35.0,
        }

        score -= risk_penalty.get(risk_level, 0.0)

        return round(
            max(0.0, min(score, 100.0)),
            2
        )

    def calculate(
        self,
        evidence_records: List[Dict[str, Any]]
    ) -> float:

        successful_records = [
            record
            for record in evidence_records
            if record.get("retrieval_status") == "success"
        ]

        if not successful_records:
            return 0.0

        record_scores = [
            self._record_score(record)
            for record in successful_records
        ]

        if not record_scores:
            return 0.0

        average_score = sum(record_scores) / len(record_scores)

        verified_support_count = len(
            [
                record
                for record in successful_records
                if record.get("can_support_verified_answer", True)
            ]
        )

        if verified_support_count >= 3:
            average_score += 6.0

        elif verified_support_count == 2:
            average_score += 3.0

        elif verified_support_count == 1:
            average_score -= 3.0

        return round(
            max(0.0, min(average_score, 100.0)),
            2
        )