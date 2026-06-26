"""
=========================================================
MODULE: Answer Length Planner

Project:
Authentic AI Search

Purpose:
Decide how detailed an answer should be.

Version:
1.0.0
=========================================================
"""

from typing import Dict


class AnswerLengthPlanner:

    SHORT_KEYWORDS = {
        "what is",
        "who is",
        "define",
        "meaning of",
        "full form",
    }

    DETAILED_KEYWORDS = {
        "explain",
        "describe",
        "how",
        "why",
        "advantages",
        "disadvantages",
        "benefits",
        "limitations",
        "working",
        "process",
        "architecture",
        "history",
    }

    RESEARCH_KEYWORDS = {
        "research",
        "report",
        "analysis",
        "compare",
        "comparison",
        "case study",
        "white paper",
        "complete guide",
        "everything about",
    }

    def plan(
        self,
        query_text: str,
    ) -> Dict:

        q = query_text.lower().strip()

        # Research Mode
        if any(word in q for word in self.RESEARCH_KEYWORDS):
            return {
                "answer_depth": "research",
                "max_claims": 12,
                "max_paragraphs": 12,
                "style": "research",
            }

        # Detailed Mode
        if any(word in q for word in self.DETAILED_KEYWORDS):
            return {
                "answer_depth": "detailed",
                "max_claims": 8,
                "max_paragraphs": 6,
                "style": "explanatory",
            }

        # Short Definitions
        if any(q.startswith(word) for word in self.SHORT_KEYWORDS):
            return {
                "answer_depth": "normal",
                "max_claims": 4,
                "max_paragraphs": 3,
                "style": "definition",
            }

        # Default
        return {
            "answer_depth": "normal",
            "max_claims": 5,
            "max_paragraphs": 4,
            "style": "general",
        }