"""
=========================================================
MODULE: Answer Quality Model

Project:
Authentic AI Search

Purpose:
Evaluate final answer quality.

Version:
2.0.0
=========================================================
"""

from typing import Any, Dict


class AnswerQualityModel:
    """
    Lightweight quality evaluator.

    This model does NOT generate answers.

    It only evaluates:
    - completeness
    - evidence coverage
    - answer length
    - citation support
    """

    MIN_ACCEPTABLE_LENGTH = 80

    def evaluate(
        self,
        answer_text: str,
        evidence_records: list[dict[str, Any]],
        citation_count: int = 0
    ) -> Dict[str, Any]:

        answer_length = len(
            answer_text.strip()
        )

        verified_evidence_count = len(
            [
                record
                for record in evidence_records
                if record.get(
                    "retrieval_status"
                ) == "success"
            ]
        )

        completeness_score = min(
            100.0,
            answer_length / 8
        )

        evidence_score = min(
            100.0,
            verified_evidence_count * 20
        )

        citation_score = min(
            100.0,
            citation_count * 25
        )

        final_quality_score = (
            completeness_score * 0.40
            + evidence_score * 0.40
            + citation_score * 0.20
        )

        if final_quality_score >= 85:
            quality_level = "excellent"

        elif final_quality_score >= 70:
            quality_level = "good"

        elif final_quality_score >= 50:
            quality_level = "acceptable"

        else:
            quality_level = "weak"

        return {
            "quality_score": round(
                final_quality_score,
                2
            ),
            "quality_level": quality_level,
            "answer_length": answer_length,
            "verified_evidence_count":
                verified_evidence_count,
            "citation_count":
                citation_count,
            "sufficient_length":
                answer_length
                >= self.MIN_ACCEPTABLE_LENGTH,
        }