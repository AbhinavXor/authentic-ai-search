"""
=========================================================
MODULE: Feedback Engine

Project:
Authentic AI Search

Purpose:
Collect and process user feedback.

Author:
Abhinav

Version:
1.0.0
=========================================================
"""

from datetime import datetime, UTC
from typing import Any, Dict, Optional
from uuid import uuid4


class FeedbackEngine:
    """
    Feedback Engine

    Current:
    - Builds normalized feedback records
    - Calculates feedback weight

    Future:
    - Database storage
    - Reputation updates
    - ML ranking signals
    """

    VALID_FEEDBACK_TYPES = {
        "upvote",
        "downvote",
        "report",
        "neutral"
    }

    def normalize_feedback_type(
        self,
        feedback_type: str
    ) -> str:
        """
        Normalize feedback type.
        """

        if not feedback_type:
            return "neutral"

        normalized = (
            feedback_type
            .strip()
            .lower()
        )

        if normalized not in self.VALID_FEEDBACK_TYPES:
            return "neutral"

        return normalized

    def build_feedback_record(
        self,
        query: str,
        answer: str,
        feedback_type: str,
        answer_id: Optional[str] = None,
        user_comment: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Build feedback record.
        """

        normalized_feedback_type = (
            self.normalize_feedback_type(
                feedback_type
            )
        )

        return {
            "feedback_id": str(uuid4()),
            "answer_id": answer_id,
            "query": query,
            "answer": answer,
            "feedback_type": normalized_feedback_type,
            "feedback_weight": self.calculate_feedback_weight(
                normalized_feedback_type
            ),
            "user_comment": user_comment,
            "metadata": metadata or {},
            "created_at": datetime.now(
                UTC
            ).isoformat()
        }

    def calculate_feedback_weight(
        self,
        feedback_type: str
    ) -> float:
        """
        Convert feedback into score weight.
        """

        feedback_type = (
            self.normalize_feedback_type(
                feedback_type
            )
        )

        if feedback_type == "upvote":
            return 1.0

        if feedback_type == "downvote":
            return -1.0

        if feedback_type == "report":
            return -2.0

        return 0.0