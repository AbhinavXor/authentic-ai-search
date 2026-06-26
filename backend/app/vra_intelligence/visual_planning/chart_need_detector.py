"""
=========================================================
MODULE: Chart Need Detector

Project:
Authentic AI Search

Engine:
VRA Intelligence

Purpose:
Detect whether a user query needs visual/chart output.

Author:
Abhinav

Version:
1.0.0
=========================================================
"""

from typing import Any, Dict


class ChartNeedDetector:
    """
    Detects whether a query needs chart/visual output.
    """

    def __init__(self) -> None:
        self.visual_keywords = [
            "chart",
            "graph",
            "plot",
            "visualize",
            "trend",
            "comparison",
            "compare",
            "timeline",
            "table",
            "dashboard",
            "growth",
            "decline",
            "increase",
            "decrease",
            "percentage",
            "statistics",
            "data"
        ]

    def detect(
        self,
        query: str
    ) -> Dict[str, Any]:
        """
        Detect visual need.
        """

        query_lower = query.lower()

        matched_keywords = [
            keyword
            for keyword in self.visual_keywords
            if keyword in query_lower
        ]

        return {
            "needs_visual": len(matched_keywords) > 0,
            "matched_visual_keywords": matched_keywords
        }