"""
=========================================================
MODULE: Trust Timeline

Project:
Authentic AI Search

Engine:
VRA Search Engine

Purpose:
Build trust timeline entries for sources and evidence.

Author:
Abhinav

Version:
1.0.0
=========================================================
"""

from datetime import datetime, timezone
from typing import Any, Dict, List


class TrustTimelineBuilder:
    """
    Builds a trust timeline for evidence records.

    Current MVP:
    - Uses current request evidence only.

    Future:
    - Use historical database records.
    - Track source trust changes over time.
    - Track claim evolution over time.
    """

    def __init__(self) -> None:
        pass

    def _now_iso(self) -> str:
        """
        Return current UTC timestamp.
        """

        return datetime.now(
            timezone.utc
        ).isoformat()

    def _build_event(
        self,
        record: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Build one timeline event.
        """

        retrieval_status = record.get(
            "retrieval_status",
            "unknown"
        )

        source_name = record.get(
            "source_name"
        )

        domain = record.get(
            "domain"
        )

        event_type = (
            "source_verified"
            if retrieval_status == "success"
            else "source_failed"
        )

        event_label = (
            "Source verified successfully"
            if retrieval_status == "success"
            else "Source could not be reached"
        )

        return {
            "timestamp": self._now_iso(),
            "event_type": event_type,
            "event_label": event_label,
            "source": source_name,
            "domain": domain,
            "url": record.get("source_url"),
            "claim": record.get("extracted_claim"),
            "retrieval_status": retrieval_status,
            "authority_score": record.get(
                "authority_score",
                0
            ),
            "reputation_score": record.get(
                "reputation_score",
                0
            ),
            "feedback_score": record.get(
                "feedback_score",
                50
            ),
            "source_reliability_score": record.get(
                "source_reliability_score",
                0
            ),
            "freshness_score": record.get(
                "freshness_score",
                0
            )
        }

    def build(
        self,
        evidence_records: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """
        Build timeline from evidence records.
        """

        timeline = []

        for record in evidence_records:
            timeline.append(
                self._build_event(record)
            )

        timeline.sort(
            key=lambda item: item.get("timestamp", ""),
            reverse=True
        )

        return timeline