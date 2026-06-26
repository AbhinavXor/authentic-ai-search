"""
=========================================================
MODULE: Output Quality Checker

Project:
Authentic AI Search

Engine:
VRA Intelligence

Purpose:
Estimate overall answer quality.

Author:
Abhinav

Version:
1.0.0
=========================================================
"""

from typing import Dict, Any


class OutputQualityChecker:

    def evaluate(
        self,
        answer: str
    ) -> Dict[str, Any]:

        answer_length = len(
            answer.strip()
        )

        quality_score = min(
            answer_length / 10,
            100
        )

        if quality_score >= 80:
            level = "excellent"

        elif quality_score >= 60:
            level = "good"

        elif quality_score >= 40:
            level = "fair"

        else:
            level = "poor"

        return {
            "quality_score": round(
                quality_score,
                2
            ),
            "quality_level": level
        }