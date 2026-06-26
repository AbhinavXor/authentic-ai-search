"""
=========================================================
MODULE: Answer Strategy Selector

Project:
Authentic AI Search

Engine:
VRA Intelligence

Purpose:
Select optimal answer generation strategy.

Author:
Abhinav

Version:
1.0.0
=========================================================
"""

from typing import Dict, Any


class AnswerStrategySelector:
    """
    Select answer generation strategy.

    Future:
    - VIAA Integration
    - Multi-worker routing
    - Cost optimization
    - Local LLM routing
    - API fallback routing
    """

    def __init__(self) -> None:

        self.chart_keywords = {
            "graph",
            "chart",
            "plot",
            "visualize",
            "trend"
        }

        self.pdf_keywords = {
            "pdf",
            "report",
            "document"
        }

        self.code_keywords = {
            "code",
            "python",
            "java",
            "javascript",
            "program"
        }

        self.math_keywords = {
            "solve",
            "equation",
            "math",
            "physics",
            "chemistry",
            "formula"
        }

        self.image_keywords = {
            "image",
            "photo",
            "picture",
            "analyze image"
        }

    def select(
        self,
        query: str
    ) -> Dict[str, Any]:
        """
        Select answer strategy.
        """

        query_lower = query.lower()

        strategy = "direct_answer"

        if any(
            keyword in query_lower
            for keyword in self.chart_keywords
        ):
            strategy = "chart_generation"

        elif any(
            keyword in query_lower
            for keyword in self.pdf_keywords
        ):
            strategy = "pdf_generation"

        elif any(
            keyword in query_lower
            for keyword in self.code_keywords
        ):
            strategy = "code_generation"

        elif any(
            keyword in query_lower
            for keyword in self.math_keywords
        ):
            strategy = "reasoning_mode"

        elif any(
            keyword in query_lower
            for keyword in self.image_keywords
        ):
            strategy = "image_analysis"

        return {
            "strategy": strategy,
            "query": query
        }