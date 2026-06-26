"""
=========================================================
MODULE: Citation Hover Builder

Project:
Authentic AI Search

Engine:
VRA Search Engine

Purpose:
Build citation hover evidence cards for frontend.

Author:
Abhinav

Version:
1.0.0
=========================================================
"""

from typing import Any, Dict, List


class CitationHoverBuilder:
    """
    Builds frontend-friendly citation hover cards.

    This module is intentionally independent.
    It will be integrated into pipeline.py later.
    """

    def __init__(
        self,
        max_snippet_chars: int = 500
    ) -> None:
        self.max_snippet_chars = max_snippet_chars

    def _build_snippet(
        self,
        record: Dict[str, Any]
    ) -> str:
        """
        Build citation evidence snippet.
        """

        snippet = (
            record.get("compressed_evidence")
            or record.get("extracted_claim")
            or record.get("page_description")
            or record.get("page_text")
            or ""
        )

        snippet = " ".join(
            str(snippet).split()
        )

        return snippet[: self.max_snippet_chars]

    def build(
        self,
        evidence_records: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """
        Build citation hover cards from verified records.
        """

        hover_cards = []

        for record in evidence_records:
            if record.get("retrieval_status") != "success":
                continue

            hover_cards.append(
                {
                    "source": record.get("source_name"),
                    "domain": record.get("domain"),
                    "url": record.get("source_url"),
                    "claim": record.get("extracted_claim"),
                    "evidence_snippet": self._build_snippet(record),
                    "authority_score": record.get("authority_score", 0),
                    "reputation_score": record.get("reputation_score", 0),
                    "feedback_score": record.get("feedback_score", 50),
                    "source_reliability_score": record.get(
                        "source_reliability_score",
                        0
                    ),
                    "freshness_score": record.get("freshness_score", 0)
                }
            )

        return hover_cards