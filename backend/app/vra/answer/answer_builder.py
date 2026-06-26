"""
=========================================================
MODULE: Answer Builder

Project:
Authentic AI Search

Engine:
Verified Resource Algorithm (VRA)

Purpose:
Build user-friendly answers using verified sources.

Important:
This module does not verify facts.
It only formats the final response after VRA scoring.

Author:
Abhinav

Version:
0.1.0
=========================================================
"""

from typing import Any, Dict, List


class AnswerBuilder:
    """
    Builds final user-facing answer text.

    Current MVP:
    - Creates a transparent answer
    - Mentions selected trusted sources

    Future:
    - Hindi/Hinglish response
    - Conflict warning
    - Freshness warning
    - Citation formatting
    """

    def build_answer(
        self,
        query_text: str,
        sources: List[Dict[str, Any]],
        trust_score: float
    ) -> str:
        """
        Build final answer text.
        """

        if not sources:
            return (
                "Verified source nahi mila. "
                "Isliye confident answer nahi de sakta."
            )

        source_names = ", ".join(
            source.get("name", "Unknown Source")
            for source in sources
        )

        return (
            f"VRA ne query receive ki: '{query_text}'. "
            f"Is answer ke liye trusted sources select hue: {source_names}. "
            f"Current trust score: {trust_score}/100."
        )