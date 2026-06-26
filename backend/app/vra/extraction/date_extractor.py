"""
=========================================================
MODULE: Date Extractor

Project:
Authentic AI Search

Engine:
VRA Search Engine

Purpose:
Extract possible published or updated dates from
HTML/text evidence.

Author:
Abhinav

Version:
1.0.0
=========================================================
"""

import re
from datetime import datetime
from typing import Any, Dict, Optional


class DateExtractor:
    """
    Extracts date information from page metadata and text.

    This module is intentionally independent.
    It will be integrated into pipeline.py later.
    """

    def __init__(self) -> None:
        self.date_patterns = [
            r"\b\d{4}-\d{2}-\d{2}\b",
            r"\b\d{2}/\d{2}/\d{4}\b",
            r"\b\d{1,2}\s+[A-Za-z]+\s+\d{4}\b",
            r"\b[A-Za-z]+\s+\d{1,2},\s+\d{4}\b",
            r"\b\d{1,2}-\d{1,2}-\d{4}\b",
        ]

        self.metadata_keys = [
            "published_date",
            "datePublished",
            "dateModified",
            "lastModified",
            "article:published_time",
            "article:modified_time",
            "og:updated_time",
            "dc.date",
            "dc.date.created",
            "dc.date.modified",
            "modified",
            "updated"
        ]

    def _normalize_date(
        self,
        raw_date: str
    ) -> Optional[str]:
        """
        Normalize date into YYYY-MM-DD if possible.
        """

        if not raw_date:
            return None

        raw_date = raw_date.strip()

        possible_formats = [
            "%Y-%m-%d",
            "%d/%m/%Y",
            "%m/%d/%Y",
            "%d %B %Y",
            "%d %b %Y",
            "%B %d, %Y",
            "%b %d, %Y",
            "%d-%m-%Y",
            "%m-%d-%Y",
        ]

        iso_match = re.search(
            r"\d{4}-\d{2}-\d{2}",
            raw_date
        )

        if iso_match:
            return iso_match.group(0)

        for date_format in possible_formats:
            try:
                parsed_date = datetime.strptime(
                    raw_date,
                    date_format
                )

                return parsed_date.strftime(
                    "%Y-%m-%d"
                )

            except ValueError:
                continue

        return None

    def extract_from_metadata(
        self,
        metadata: Dict[str, Any]
    ) -> Optional[str]:
        """
        Extract date from metadata dictionary.
        """

        if not metadata:
            return None

        for key in self.metadata_keys:
            value = metadata.get(key)

            if not value:
                continue

            if isinstance(value, list):
                value = value[0] if value else None

            normalized_date = self._normalize_date(
                str(value)
            )

            if normalized_date:
                return normalized_date

        return None

    def extract_from_text(
        self,
        text: str
    ) -> Optional[str]:
        """
        Extract date from raw text.
        """

        if not text:
            return None

        for pattern in self.date_patterns:
            match = re.search(
                pattern,
                text
            )

            if not match:
                continue

            normalized_date = self._normalize_date(
                match.group(0)
            )

            if normalized_date:
                return normalized_date

        return None

    def extract(
        self,
        record: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Extract date from evidence record.
        """

        metadata = record.get("metadata", {})
        page_text = record.get("page_text", "")
        page_description = record.get("page_description", "")

        extracted_date = self.extract_from_metadata(
            metadata
        )

        if not extracted_date:
            extracted_date = self.extract_from_text(
                page_description
            )

        if not extracted_date:
            extracted_date = self.extract_from_text(
                page_text
            )

        return {
            "published_date": extracted_date,
            "date_status": (
                "found"
                if extracted_date
                else "not_found"
            )
        }

    def enrich_records(
        self,
        evidence_records: list[Dict[str, Any]]
    ) -> list[Dict[str, Any]]:
        """
        Add extracted date info to records.
        """

        updated_records = []

        for record in evidence_records:
            result = self.extract(record)

            if result.get("published_date"):
                record["published_date"] = result.get(
                    "published_date"
                )

            record["date_status"] = result.get(
                "date_status",
                "not_found"
            )

            updated_records.append(record)

        return updated_records