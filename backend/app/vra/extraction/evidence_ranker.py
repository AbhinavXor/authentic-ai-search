"""
=========================================================
MODULE: Evidence Ranker

Project:
Authentic AI Search

Engine:
VRA Search Engine

Purpose:
Rank evidence records by relevance, trust, reliability,
freshness, and claim quality.

Author:
Abhinav

Version:
1.0.0
=========================================================
"""

import re
from typing import Any, Dict, List


class EvidenceRanker:
    """
    Rank evidence records for better answer generation.
    """

    def __init__(self) -> None:
        pass

    def _normalize_text(
        self,
        text: str
    ) -> str:
        """
        Normalize text.
        """

        if not text:
            return ""

        text = text.lower()

        text = re.sub(
            r"[^a-z0-9\s]",
            " ",
            text
        )

        text = re.sub(
            r"\s+",
            " ",
            text
        )

        return text.strip()

    def _term_overlap_score(
        self,
        query_text: str,
        evidence_text: str
    ) -> float:
        """
        Calculate query-evidence lexical overlap.
        """

        query_terms = set(
            self._normalize_text(query_text).split()
        )

        evidence_terms = set(
            self._normalize_text(evidence_text).split()
        )

        if not query_terms or not evidence_terms:
            return 0.0

        overlap = query_terms.intersection(
            evidence_terms
        )

        return (
            len(overlap)
            / len(query_terms)
        ) * 100

    def _claim_quality_score(
        self,
        record: Dict[str, Any]
    ) -> float:
        """
        Score extracted claim quality.
        """

        claim = record.get("extracted_claim") or ""

        if not claim:
            return 0.0

        claim_length = len(claim)

        if claim_length < 20:
            return 30.0

        if claim_length < 80:
            return 70.0

        return 90.0

    def score_record(
        self,
        record: Dict[str, Any],
        query_text: str
    ) -> float:
        """
        Score one evidence record.
        """

        if record.get("retrieval_status") != "success":
            return 0.0

        evidence_text = (
            record.get("compressed_evidence")
            or record.get("page_text")
            or record.get("extracted_claim")
            or ""
        )

        relevance_score = self._term_overlap_score(
            query_text=query_text,
            evidence_text=evidence_text
        )

        authority_score = float(
            record.get("authority_score", 0)
        )

        reputation_score = float(
            record.get("reputation_score", 0)
        )

        reliability_score = float(
            record.get("source_reliability_score", 0)
        )

        freshness_score = float(
            record.get("freshness_score", 0)
        )

        claim_quality_score = self._claim_quality_score(
            record
        )

        final_score = (
            relevance_score * 0.30
            + authority_score * 0.20
            + reputation_score * 0.20
            + reliability_score * 0.15
            + freshness_score * 0.05
            + claim_quality_score * 0.10
        )

        return round(
            final_score,
            2
        )

    def rank(
        self,
        evidence_records: List[Dict[str, Any]],
        query_text: str
    ) -> List[Dict[str, Any]]:
        """
        Rank evidence records.
        """

        ranked_records = []

        for record in evidence_records:
            score = self.score_record(
                record=record,
                query_text=query_text
            )

            record["evidence_rank_score"] = score

            ranked_records.append(record)

        ranked_records.sort(
            key=lambda item: item.get(
                "evidence_rank_score",
                0
            ),
            reverse=True
        )

        for index, record in enumerate(
            ranked_records,
            start=1
        ):
            record["evidence_rank"] = index

        return ranked_records