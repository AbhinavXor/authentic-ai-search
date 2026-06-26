"""
=========================================================
MODULE: Intent Detector

Project:
Authentic AI Search

Engine:
Verified Resource Algorithm (VRA)

Purpose:
Detect user query intent/category.

Author:
Abhinav

Version:
0.1.0
=========================================================
"""


class IntentDetector:
    """
    Detects basic query category.

    Current MVP:
    - Rule-based keyword detection

    Future:
    - ML classifier
    - Hindi/Hinglish intent detection
    - Legal/medical/finance modes
    """

    def detect_category(self, query_text: str) -> str:
        """
        Detect query category from text.
        """

        text = query_text.lower()

        government_keywords = [
            "population",
            "census",
            "government",
            "scheme",
            "gdp",
            "inflation",
            "unemployment"
        ]

        research_keywords = [
            "research",
            "paper",
            "study",
            "arxiv",
            "journal",
            "experiment"
        ]

        organization_keywords = [
            "un",
            "world bank",
            "who",
            "unesco",
            "united nations"
        ]

        if any(keyword in text for keyword in government_keywords):
            return "government"

        if any(keyword in text for keyword in research_keywords):
            return "research"

        if any(keyword in text for keyword in organization_keywords):
            return "official_organization"

        return "government"