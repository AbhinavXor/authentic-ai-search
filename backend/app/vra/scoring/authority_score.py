"""
=========================================================
MODULE: Authority Score Engine

Project:
Authentic AI Search

Purpose:
Calculate authority score for trusted sources.

Author:
Abhinav

Version:
0.1.0
=========================================================
"""

from typing import Any, Dict


class AuthorityScoreEngine:
    """
    Calculates source authority score.

    Current logic:
    - Uses authority_score from source registry.

    Future logic:
    - Domain reputation
    - Official source validation
    - Historical trust
    - Admin-approved source weight
    """

    def calculate(self, source: Dict[str, Any]) -> float:
        """
        Return authority score from source metadata.
        """

        score = source.get("authority_score", 0)

        return float(score)