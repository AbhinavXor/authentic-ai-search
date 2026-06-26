"""
=========================================================
MODULE: Freshness Score Engine

Project:
Authentic AI Search

Purpose:
Calculate freshness score for evidence.

Author:
Abhinav

Version:
1.1.0
=========================================================
"""

from datetime import datetime, timezone
from email.utils import parsedate_to_datetime
from typing import Any, Dict


class FreshnessScoreEngine:
    """
    Calculates freshness score for evidence records.
    """

    def _parse_date(
        self,
        date_text: str
    ) -> datetime | None:
        """
        Try parsing common web date formats.
        """

        if not date_text:
            return None

        try:
            parsed_date = parsedate_to_datetime(date_text)

            if parsed_date.tzinfo is None:
                parsed_date = parsed_date.replace(
                    tzinfo=timezone.utc
                )

            return parsed_date

        except Exception:
            pass

        try:
            normalized = date_text.replace("Z", "+00:00")
            parsed_date = datetime.fromisoformat(normalized)

            if parsed_date.tzinfo is None:
                parsed_date = parsed_date.replace(
                    tzinfo=timezone.utc
                )

            return parsed_date

        except Exception:
            return None

    def calculate(
        self,
        record: Dict[str, Any]
    ) -> float:
        """
        Return freshness score.
        """

        result = self.evaluate(record)

        return result["freshness_score"]

    def evaluate(
        self,
        record: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Return freshness score and status.
        """

        published_date = record.get("published_date")

        if not published_date:
            return {
                "freshness_score": 40.0,
                "freshness_status": "unknown"
            }

        parsed_date = self._parse_date(published_date)

        if not parsed_date:
            return {
                "freshness_score": 40.0,
                "freshness_status": "unknown"
            }

        now = datetime.now(timezone.utc)

        age_days = (now - parsed_date).days

        if age_days <= 7:
            return {
                "freshness_score": 100.0,
                "freshness_status": "very_fresh"
            }

        if age_days <= 30:
            return {
                "freshness_score": 90.0,
                "freshness_status": "fresh"
            }

        if age_days <= 180:
            return {
                "freshness_score": 75.0,
                "freshness_status": "recent"
            }

        if age_days <= 365:
            return {
                "freshness_score": 60.0,
                "freshness_status": "aging"
            }

        return {
            "freshness_score": 40.0,
            "freshness_status": "stale"
        }