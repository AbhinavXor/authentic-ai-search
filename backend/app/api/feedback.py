"""
=========================================================
MODULE: Feedback API

Project:
Authentic AI Search

Purpose:
Collect and persist user feedback.

Author:
Abhinav

Version:
1.2.0
=========================================================
"""

from fastapi import APIRouter
from pydantic import BaseModel

from backend.app.vra.feedback.feedback_engine import (
    FeedbackEngine
)
from backend.app.storage.feedback_store import (
    FeedbackStore
)
from backend.app.storage.source_stats_store import (
    SourceStatsStore
)


router = APIRouter()

feedback_engine = FeedbackEngine()
feedback_store = FeedbackStore()
source_stats_store = SourceStatsStore()


class FeedbackRequest(BaseModel):
    """
    Request body for feedback submission.
    """

    query: str
    answer: str
    feedback_type: str
    answer_id: str | None = None
    user_comment: str | None = None
    source_domain: str | None = None
    source_name: str | None = None


@router.post("/feedback")
def submit_feedback(
    request: FeedbackRequest
) -> dict:
    """
    Submit and persist user feedback.
    """

    feedback_record = feedback_engine.build_feedback_record(
        query=request.query,
        answer=request.answer,
        feedback_type=request.feedback_type,
        answer_id=request.answer_id,
        user_comment=request.user_comment,
        metadata={
            "source_domain": request.source_domain,
            "source_name": request.source_name
        }
    )

    saved_record = feedback_store.save(
        feedback_record
    )

    source_stats = {}

    if request.source_domain:
        source_stats = (
            source_stats_store.update_feedback_stats(
                domain=request.source_domain,
                source_name=request.source_name,
                feedback_type=request.feedback_type
            )
        )

    return {
        "status": "success",
        "message": "Feedback saved successfully.",
        "feedback": saved_record,
        "source_stats": source_stats
    }


@router.get("/feedback/recent")
def recent_feedback() -> dict:
    """
    Return recent feedback records.
    """

    records = feedback_store.list_recent(
        limit=20
    )

    return {
        "status": "success",
        "count": len(records),
        "feedback": records
    }


@router.get("/feedback/source-stats")
def source_stats() -> dict:
    """
    Return source-level feedback statistics.
    """

    stats = source_stats_store.list_sources()

    return {
        "status": "success",
        "count": len(stats),
        "sources": stats
    }