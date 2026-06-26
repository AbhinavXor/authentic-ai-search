"""
=========================================================
MODULE: Chat API

Project:
Authentic AI Search

Purpose:
Provide POST /chat endpoint for user queries.

Author:
Abhinav

Version:
2.0.0
=========================================================
"""

from fastapi import APIRouter
from pydantic import BaseModel

from backend.app.vra.pipeline import VRAPipeline
from backend.app.vra.types import UserQuery


router = APIRouter()


class ChatRequest(BaseModel):
    """
    Request body for chat/search query.
    """

    query: str
    debug: bool = False


@router.post("/chat")
def chat(request: ChatRequest) -> dict:
    """
    Process user query through VRA pipeline.
    """

    pipeline = VRAPipeline()

    user_query = UserQuery(
        query_text=request.query
    )

    result = pipeline.process_query(user_query)

    response = {
        "answer": result.answer,

        "answer_type": result.answer_type,
        "answer_mode": result.answer_mode,

        "verification_status": result.verification_status,
        "verification_badge": result.verification_badge,
        "verification_summary": result.verification_summary,

        "trust_score": result.trust_score,
        "confidence_score": result.confidence_score,
        "agreement_score": result.agreement_score,

        "answer_quality_score": result.answer_quality_score,
        "answer_quality_level": result.answer_quality_level,

        "safety_score": result.safety_score,
        "safety_level": result.safety_level,
        "matched_safety_keywords": result.matched_safety_keywords,

        "hallucination_risk_score": result.hallucination_risk_score,
        "hallucination_risk_level": result.hallucination_risk_level,

        "consensus_status": result.consensus_status,
        "claim_count": result.claim_count,
        "unique_claim_count": result.unique_claim_count,

        "source_count": result.source_count,
        "verified_source_count": result.verified_source_count,
        "failed_source_count": result.failed_source_count,

        "sources": [
            {
                "title": source.title,
                "url": source.url,
                "domain": source.domain,
                "source_type": source.source_type,
                "authority_score": source.authority_score,
                "freshness_score": source.freshness_score,
                "verified": source.verified,
                "is_official": source.is_official,
                "is_trusted": source.is_trusted,
                "source_category": source.source_category,
                "authenticity_category": source.authenticity_category,
                "discovery_score": source.discovery_score,
                "reputation_score": source.reputation_score,
                "retrieval_status": source.retrieval_status,
            }
            for source in result.sources
        ],

        "source_cards": result.source_cards,
        "citations": result.citations,

        "warning_message": result.warning_message,

        "query_intent": result.query_intent,
        "is_personal_response": result.is_personal_response,
        "used_ai_reasoning": result.used_ai_reasoning,
    }

    if request.debug:
        response.update(
            {
                "evidence_summary": result.evidence_summary,
                "evidence_graph": result.evidence_graph,
                "claim_lineage": result.claim_lineage,
                "ranked_sources": result.ranked_sources,
                "claim_groups": result.claim_groups,
                "contradiction_result": result.contradiction_result,
                "evidence_clusters": result.evidence_clusters,
                "multi_hop_chains": result.multi_hop_chains,
                "evidence_records": result.evidence_records,
                "verified_sources": result.verified_sources,
                "failed_sources": result.failed_sources,
            }
        )

    return response