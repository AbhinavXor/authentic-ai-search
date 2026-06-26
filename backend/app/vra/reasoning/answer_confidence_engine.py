"""
=========================================================
MODULE: Answer Confidence Engine

Project:
Authentic AI Search

Engine:
VRA Search Engine

Purpose:
Calculate final answer confidence score.

Author:
Abhinav

Version:
1.0.0
=========================================================
"""

from typing import Any, Dict, List


class AnswerConfidenceEngine:
    """
    Calculate final answer confidence.
    """

    def __init__(self) -> None:
        pass

    def calculate(
        self,
        trust_score: float,
        consensus_score: float,
        disagreement_score: float,
        source_scores: List[float]
    ) -> Dict[str, Any]:
        """
        Calculate answer confidence.
        """

        average_source_score = (
            sum(source_scores) / len(source_scores)
            if source_scores
            else 0.0
        )

        confidence_score = (
            trust_score * 0.35
            + consensus_score * 0.30
            + average_source_score * 0.25
            - disagreement_score * 0.10
        )

        confidence_score = max(
            0.0,
            min(
                100.0,
                round(confidence_score, 2)
            )
        )

        if confidence_score >= 90:
            level = "very_high"

        elif confidence_score >= 75:
            level = "high"

        elif confidence_score >= 60:
            level = "medium"

        elif confidence_score >= 40:
            level = "low"

        else:
            level = "very_low"

        if confidence_score >= 90:
            recommendation = "direct_answer"

        elif confidence_score >= 70:
            recommendation = "verified_answer"

        elif confidence_score >= 40:
            recommendation = "partial_verification"

        else:
            recommendation = "research_required"

        return {
            "answer_confidence_score": confidence_score,
            "answer_confidence_level": level,
            "answer_recommendation": recommendation,
            "average_source_score": round(
                average_source_score,
                2
            )
        }