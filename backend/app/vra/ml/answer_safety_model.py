"""
=========================================================
MODULE: Answer Safety Model

Project:
Authentic AI Search

Purpose:
Classify safety sensitivity without over-blocking normal answers.

Version:
2.0.0
=========================================================
"""

from typing import Any, Dict


class AnswerSafetyModel:
    """
    Rule-based safety classifier.

    Important:
    - Does not block by itself.
    - Only labels risk level.
    - Personal/emotional support should not become factual verification.
    """

    HIGH_RISK_KEYWORDS = {
        "suicide",
        "self harm",
        "kill myself",
        "harm myself",
        "weapon",
        "explosive",
        "bomb",
        "poison",
        "overdose",
    }

    MEDIUM_RISK_KEYWORDS = {
        "medicine",
        "drug",
        "dose",
        "diagnosis",
        "symptom",
        "legal advice",
        "invest",
        "stock",
        "loan",
        "election",
        "vote",
        "depression",
        "anxiety",
        "panic",
        "mental health",
    }

    PERSONAL_SUPPORT_KEYWORDS = {
        "i am not feeling good",
        "i feel sad",
        "i am sad",
        "i feel lonely",
        "i am lonely",
        "i feel depressed",
        "i am depressed",
        "i feel anxious",
        "i am anxious",
        "i need help",
    }

    def _matched_keywords(
        self,
        text: str,
        keywords: set[str]
    ) -> list[str]:
        return [
            keyword
            for keyword in keywords
            if keyword in text
        ]

    def evaluate(
        self,
        query_text: str,
        answer_text: str
    ) -> Dict[str, Any]:

        combined_text = f"{query_text} {answer_text}".lower()

        high_matches = self._matched_keywords(
            combined_text,
            self.HIGH_RISK_KEYWORDS
        )

        if high_matches:
            return {
                "safety_level": "high_risk",
                "safety_score": 35.0,
                "matched_safety_keywords": high_matches,
                "requires_disclaimer": True,
                "personal_support": False,
            }

        personal_matches = self._matched_keywords(
            combined_text,
            self.PERSONAL_SUPPORT_KEYWORDS
        )

        medium_matches = self._matched_keywords(
            combined_text,
            self.MEDIUM_RISK_KEYWORDS
        )

        if personal_matches:
            return {
                "safety_level": "supportive_context",
                "safety_score": 85.0,
                "matched_safety_keywords": personal_matches,
                "requires_disclaimer": False,
                "personal_support": True,
            }

        if medium_matches:
            return {
                "safety_level": "medium_risk",
                "safety_score": 70.0,
                "matched_safety_keywords": medium_matches,
                "requires_disclaimer": True,
                "personal_support": False,
            }

        return {
            "safety_level": "low_risk",
            "safety_score": 95.0,
            "matched_safety_keywords": [],
            "requires_disclaimer": False,
            "personal_support": False,
        }