"""
=========================================================
MODULE: Evidence Compressor

Project:
Authentic AI Search

Engine:
VRA Search Engine

Purpose:
Compress raw fetched evidence into compact,
LLM-safe, source-grounded evidence snippets.

Author:
Abhinav

Version:
1.0.0
=========================================================
"""

import re
from typing import Any, Dict, List


class EvidenceCompressor:
    """
    Compress evidence records for answer generation.

    This module is intentionally independent.
    It will be integrated into pipeline.py later.
    """

    def __init__(
        self,
        max_snippet_chars: int = 1200,
        max_sentences: int = 6
    ) -> None:
        self.max_snippet_chars = max_snippet_chars
        self.max_sentences = max_sentences

    def _clean_text(
        self,
        text: str
    ) -> str:
        """
        Clean raw text.
        """

        if not text:
            return ""

        cleaned = re.sub(
            r"\s+",
            " ",
            text
        ).strip()

        return cleaned

    def _split_sentences(
        self,
        text: str
    ) -> List[str]:
        """
        Split text into simple sentence chunks.
        """

        if not text:
            return []

        sentences = re.split(
            r"(?<=[.!?])\s+",
            text
        )

        return [
            sentence.strip()
            for sentence in sentences
            if sentence.strip()
        ]

    def _score_sentence(
        self,
        sentence: str,
        query_text: str,
        claim: str
    ) -> int:
        """
        Score sentence relevance using simple lexical overlap.
        """

        score = 0

        query_terms = set(
            query_text.lower().split()
        )

        claim_terms = set(
            claim.lower().split()
        )

        sentence_terms = set(
            sentence.lower().split()
        )

        score += len(
            query_terms.intersection(sentence_terms)
        ) * 3

        score += len(
            claim_terms.intersection(sentence_terms)
        ) * 2

        if len(sentence) < 40:
            score -= 2

        if len(sentence) > 400:
            score -= 1

        return score

    def compress_record(
        self,
        record: Dict[str, Any],
        query_text: str
    ) -> Dict[str, Any]:
        """
        Compress a single evidence record.
        """

        if record.get("retrieval_status") != "success":
            record["compressed_evidence"] = ""
            record["compressed_evidence_status"] = "skipped_failed_source"
            return record

        page_text = (
            record.get("page_text")
            or record.get("content")
            or record.get("text")
            or ""
        )

        claim = record.get("extracted_claim") or ""

        cleaned_text = self._clean_text(
            page_text
        )

        if not cleaned_text:
            record["compressed_evidence"] = claim
            record["compressed_evidence_status"] = (
                "fallback_to_claim"
            )
            return record

        sentences = self._split_sentences(
            cleaned_text
        )

        scored_sentences = [
            (
                self._score_sentence(
                    sentence=sentence,
                    query_text=query_text,
                    claim=claim
                ),
                sentence
            )
            for sentence in sentences
        ]

        scored_sentences.sort(
            key=lambda item: item[0],
            reverse=True
        )

        selected_sentences = [
            sentence
            for score, sentence in scored_sentences
            if score > 0
        ][: self.max_sentences]

        if not selected_sentences:
            selected_sentences = sentences[: self.max_sentences]

        compressed = " ".join(
            selected_sentences
        )

        compressed = compressed[: self.max_snippet_chars]

        record["compressed_evidence"] = compressed
        record["compressed_evidence_status"] = "compressed"

        return record

    def compress_records(
        self,
        evidence_records: List[Dict[str, Any]],
        query_text: str
    ) -> List[Dict[str, Any]]:
        """
        Compress multiple evidence records.
        """

        compressed_records = []

        for record in evidence_records:
            compressed_records.append(
                self.compress_record(
                    record=record,
                    query_text=query_text
                )
            )

        return compressed_records