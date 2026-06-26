"""
=========================================================
MODULE: Completeness Checker

Project:
Authentic AI Search

Engine:
VRA Intelligence

Purpose:
Check answer completeness.

Author:
Abhinav

Version:
1.0.0
=========================================================
"""

from typing import Dict, Any


class CompletenessChecker:

    def evaluate(
        self,
        answer: str
    ) -> Dict[str, Any]:

        word_count = len(
            answer.split()
        )

        completeness_score = min(
            word_count,
            100
        )

        return {
            "word_count": word_count,
            "completeness_score":
            completeness_score
        }