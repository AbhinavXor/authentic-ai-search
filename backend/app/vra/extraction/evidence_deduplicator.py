"""
=========================================================
MODULE: Evidence Deduplicator

Project:
Authentic AI Search

Engine:
VRA Search Engine

Purpose:
Remove duplicate evidence records and reduce
token waste before answer generation.

Author:
Abhinav

Version:
1.0.0
=========================================================
"""

import hashlib
import re

from typing import Any, Dict, List


class EvidenceDeduplicator:
    """
    Remove duplicate evidence records.
    """

    def __init__(
        self,
        similarity_threshold: float = 0.80
    ) -> None:
        self.similarity_threshold = similarity_threshold

    def _normalize_text(
        self,
        text: str
    ) -> str:
        """
        Normalize text for comparison.
        """

        if not text:
            return ""

        text = text.lower()

        text = re.sub(
            r"\s+",
            " ",
            text
        )

        text = re.sub(
            r"[^a-z0-9\s]",
            "",
            text
        )

        return text.strip()

    def _content_hash(
        self,
        text: str
    ) -> str:
        """
        Generate content hash.
        """

        normalized = self._normalize_text(
            text
        )

        return hashlib.sha256(
            normalized.encode("utf-8")
        ).hexdigest()

    def deduplicate(
        self,
        evidence_records: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """
        Remove duplicate evidence.
        """

        unique_records = []

        seen_hashes = set()

        for record in evidence_records:

            content = (
                record.get("compressed_evidence")
                or record.get("page_text")
                or record.get("extracted_claim")
                or ""
            )

            content_hash = self._content_hash(
                content[:3000]
            )

            if content_hash in seen_hashes:
                continue

            seen_hashes.add(
                content_hash
            )

            unique_records.append(
                record
            )

        return unique_records

    def enrich_records(
        self,
        evidence_records: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Return deduplication report.
        """

        original_count = len(
            evidence_records
        )

        unique_records = self.deduplicate(
            evidence_records
        )

        unique_count = len(
            unique_records
        )

        duplicate_count = (
            original_count
            - unique_count
        )

        return {
            "records": unique_records,
            "original_count": original_count,
            "unique_count": unique_count,
            "duplicate_count": duplicate_count
        }