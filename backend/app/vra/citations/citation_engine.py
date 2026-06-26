"""
=========================================================
MODULE: Citation Engine

Project:
Authentic AI Search

Purpose:
Build structured citations, source cards, and inline labels.

Version:
3.2.0
=========================================================
"""

import re
from typing import Any, Dict, List


class CitationEngine:
    """
    Builds citation objects for frontend/API.
    """

    def _safe_float(
        self,
        value: Any,
        default: float = 0.0
    ) -> float:
        try:
            if value is None:
                return default

            return float(value)

        except Exception:
            return default

    def _safe_text(
        self,
        value: Any
    ) -> str:
        if value is None:
            return ""

        return str(value).strip()

    def _is_verified_source(
        self,
        record: Dict[str, Any]
    ) -> bool:
        if record.get("retrieval_status") != "success":
            return False

        if record.get("can_support_verified_answer") is True:
            return True

        if record.get("is_official") is True:
            return True

        if record.get("is_trusted") is True:
            return True

        authority_score = self._safe_float(
            record.get("authority_score")
        )

        official_confidence = self._safe_float(
            record.get("official_confidence_score")
        )

        rank_score = self._safe_float(
            record.get("rank_score")
        )

        return (
            authority_score >= 85
            or official_confidence >= 85
            or rank_score >= 85
        )

    def _sort_records(
        self,
        evidence_records: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        return sorted(
            evidence_records,
            key=lambda record: (
                self._safe_float(record.get("rank_score")),
                self._safe_float(record.get("authority_score")),
                self._safe_float(record.get("relevance_score")),
                self._safe_float(record.get("official_confidence_score")),
            ),
            reverse=True
        )

    def build(
        self,
        evidence_records: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        citations: List[Dict[str, Any]] = []
        seen_urls = set()
        citation_number = 1

        for record in self._sort_records(evidence_records):
            if record.get("retrieval_status") != "success":
                continue

            source_url = self._safe_text(
                record.get("source_url")
            )

            if not source_url:
                continue

            if source_url in seen_urls:
                continue

            seen_urls.add(source_url)

            claim = (
                record.get("extracted_claim")
                or record.get("primary_claim")
                or record.get("page_description")
            )

            citations.append(
                {
                    "label": f"[{citation_number}]",
                    "citation_id": citation_number,
                    "source": record.get("source_name"),
                    "source_name": record.get("source_name"),
                    "title": record.get("page_title"),
                    "domain": record.get("domain"),
                    "url": source_url,
                    "claim": claim,
                    "supporting_claims": record.get(
                        "supporting_claims",
                        []
                    ),
                    "authority_score": self._safe_float(
                        record.get("authority_score")
                    ),
                    "rank_score": self._safe_float(
                        record.get("rank_score")
                    ),
                    "relevance_score": self._safe_float(
                        record.get("relevance_score")
                    ),
                    "official_confidence_score": self._safe_float(
                        record.get("official_confidence_score")
                    ),
                    "source_type": record.get("source_type"),
                    "source_category": record.get("source_category"),
                    "authenticity_category": record.get(
                        "authenticity_category"
                    ),
                    "is_official": record.get("is_official", False),
                    "is_trusted": record.get("is_trusted", False),
                    "verified": self._is_verified_source(record),
                    "source_risk_level": record.get("source_risk_level"),
                    "retrieval_status": record.get("retrieval_status"),
                }
            )

            citation_number += 1

        return citations

    def build_source_cards(
        self,
        evidence_records: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        cards: List[Dict[str, Any]] = []
        seen_domains = set()

        for record in self._sort_records(evidence_records):
            if record.get("retrieval_status") != "success":
                continue

            domain = self._safe_text(
                record.get("domain")
            )

            if not domain:
                continue

            if domain in seen_domains:
                continue

            seen_domains.add(domain)

            cards.append(
                {
                    "name": record.get("source_name"),
                    "title": record.get("page_title"),
                    "domain": domain,
                    "url": record.get("source_url"),
                    "verified": self._is_verified_source(record),
                    "is_official": record.get("is_official", False),
                    "is_trusted": record.get("is_trusted", False),
                    "authority_score": self._safe_float(
                        record.get("authority_score")
                    ),
                    "rank_score": self._safe_float(
                        record.get("rank_score")
                    ),
                    "relevance_score": self._safe_float(
                        record.get("relevance_score")
                    ),
                    "official_confidence_score": self._safe_float(
                        record.get("official_confidence_score")
                    ),
                    "source_type": record.get("source_type"),
                    "source_category": record.get("source_category"),
                    "authenticity_category": record.get(
                        "authenticity_category"
                    ),
                    "source_risk_level": record.get("source_risk_level"),
                    "reliability": record.get(
                        "source_reliability_level",
                        "unknown"
                    ),
                }
            )

        return cards

    def replace_citation_placeholders(
        self,
        answer_text: str,
        citations: List[Dict[str, Any]]
    ) -> str:
        """
        Replace Gemini placeholders with citation labels.

        Handles:
        - {{CITATION}}
        - [[CITATION]]
        - [[SOURCE]]
        - malformed [[SOURCE
        - malformed [[CITATION
        - duplicate labels like [1] [1] [1]
        """

        if not answer_text:
            return answer_text

        cleaned_answer = answer_text.strip()

        primary_label = (
            citations[0].get("label", "")
            if citations
            else ""
        )

        if primary_label:
            cleaned_answer = re.sub(
                r"\{\{\s*CITATION\s*\}\}",
                primary_label,
                cleaned_answer,
                flags=re.IGNORECASE,
            )

            cleaned_answer = re.sub(
                r"\[\[\s*SOURCE\s*\]?\]?",
                primary_label,
                cleaned_answer,
                flags=re.IGNORECASE,
            )

            cleaned_answer = re.sub(
                r"\[\[\s*CITATION\s*\]?\]?",
                primary_label,
                cleaned_answer,
                flags=re.IGNORECASE,
            )

            cleaned_answer = re.sub(
                r"(\[\d+\]\s*){2,}",
                primary_label + " ",
                cleaned_answer,
            )

        else:
            cleaned_answer = re.sub(
                r"\{\{\s*CITATION\s*\}\}",
                "",
                cleaned_answer,
                flags=re.IGNORECASE,
            )

            cleaned_answer = re.sub(
                r"\[\[\s*SOURCE\s*\]?\]?",
                "",
                cleaned_answer,
                flags=re.IGNORECASE,
            )

            cleaned_answer = re.sub(
                r"\[\[\s*CITATION\s*\]?\]?",
                "",
                cleaned_answer,
                flags=re.IGNORECASE,
            )

        return " ".join(cleaned_answer.split()).strip()

    def attach_inline_citation_labels(
        self,
        answer_text: str,
        citations: List[Dict[str, Any]]
    ) -> str:
        """
        Attach strongest citation only if no citation already exists.
        """

        if not answer_text:
            return answer_text

        stripped_answer = answer_text.strip()

        if not citations:
            return self.replace_citation_placeholders(
                answer_text=stripped_answer,
                citations=[]
            )

        labels = [
            citation.get("label")
            for citation in citations
            if citation.get("label")
        ]

        if any(label in stripped_answer for label in labels):
            return stripped_answer

        first_label = labels[0] if labels else ""

        if not first_label:
            return stripped_answer

        return f"{stripped_answer} {first_label}"