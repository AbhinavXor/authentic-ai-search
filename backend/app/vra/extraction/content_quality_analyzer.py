"""
=========================================================
MODULE: Content Quality Analyzer

Project:
Authentic AI Search

Engine:
VRA Search Engine

Purpose:
Analyze fetched source content quality for VRA evidence
selection and ranking.

Author:
Abhinav

Version:
1.0.0
=========================================================
"""

import re
from typing import Any, Dict, List


class ContentQualityAnalyzer:
    """
    Scores source content quality.

    This module is intentionally independent.
    It will be integrated into pipeline.py later.
    """

    def __init__(self) -> None:
        self.noise_keywords = [
            "cookie",
            "privacy policy",
            "subscribe",
            "advertisement",
            "login",
            "sign up",
            "terms of use",
            "share this",
            "follow us"
        ]

    def _clean_text(
        self,
        text: str
    ) -> str:
        """
        Normalize content text.
        """

        if not text:
            return ""

        text = re.sub(
            r"\s+",
            " ",
            text
        )

        return text.strip()

    def _word_count(
        self,
        text: str
    ) -> int:
        """
        Count words.
        """

        if not text:
            return 0

        return len(
            text.split()
        )

    def _noise_score(
        self,
        text: str
    ) -> float:
        """
        Estimate page noise.
        """

        if not text:
            return 100.0

        lowered = text.lower()

        noise_hits = sum(
            1
            for keyword in self.noise_keywords
            if keyword in lowered
        )

        return min(
            noise_hits * 12.0,
            100.0
        )

    def _length_score(
        self,
        word_count: int
    ) -> float:
        """
        Score content length.
        """

        if word_count <= 0:
            return 0.0

        if word_count < 30:
            return 20.0

        if word_count < 80:
            return 45.0

        if word_count < 200:
            return 70.0

        return 90.0

    def _claim_presence_score(
        self,
        record: Dict[str, Any]
    ) -> float:
        """
        Score claim presence.
        """

        claim = record.get("extracted_claim")

        if not claim:
            return 0.0

        if len(claim) < 20:
            return 40.0

        return 90.0

    def analyze_record(
        self,
        record: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Analyze one evidence record.
        """

        page_text = (
            record.get("page_text")
            or record.get("compressed_evidence")
            or record.get("extracted_claim")
            or ""
        )

        cleaned_text = self._clean_text(
            page_text
        )

        word_count = self._word_count(
            cleaned_text
        )

        length_score = self._length_score(
            word_count
        )

        noise_score = self._noise_score(
            cleaned_text
        )

        claim_score = self._claim_presence_score(
            record
        )

        content_quality_score = (
            length_score * 0.45
            + claim_score * 0.35
            + (100.0 - noise_score) * 0.20
        )

        content_quality_score = round(
            content_quality_score,
            2
        )

        if content_quality_score >= 75:
            quality_level = "high"

        elif content_quality_score >= 50:
            quality_level = "medium"

        elif content_quality_score >= 25:
            quality_level = "low"

        else:
            quality_level = "very_low"

        return {
            "content_word_count": word_count,
            "content_noise_score": round(noise_score, 2),
            "content_quality_score": content_quality_score,
            "content_quality_level": quality_level
        }

    def enrich_records(
        self,
        evidence_records: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """
        Add content quality fields to records.
        """

        updated_records = []

        for record in evidence_records:
            result = self.analyze_record(record)

            record.update(result)

            updated_records.append(record)

        return updated_records