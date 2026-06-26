"""
=========================================================
MODULE: VRA Core Types

Project:
Authentic AI Search

Engine:
Verified Resource Algorithm (VRA)

Purpose:
Central data structures used by the VRA system.

Author:
Abhinav

Version:
1.0.0
=========================================================
"""

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


# =========================================================
# USER QUERY
# =========================================================

@dataclass
class UserQuery:
    """
    Represents a user search query.
    """

    query_text: str
    language: str = "en"
    category: Optional[str] = None

    metadata: Dict[str, Any] = field(
        default_factory=dict
    )


# =========================================================
# SOURCE INFO
# =========================================================

@dataclass
class SourceInfo:
    """
    Represents a source discovered by VRA.
    """

    title: str
    url: str
    domain: str
    source_type: str

    authority_score: float = 0.0
    freshness_score: float = 0.0

    discovery_score: float = 0.0

    verified: bool = False

    is_official: bool = False
    is_trusted: bool = False

    source_category: str = "web"

    authenticity_category: str = "unknown"

    reputation_score: float = 0.0

    retrieval_status: str = "unknown"


# =========================================================
# VERIFICATION
# =========================================================

@dataclass
class VerificationResult:
    """
    Verification output.
    """

    verified: bool
    confidence: float

    notes: str = ""


# =========================================================
# TRUST SCORE
# =========================================================

@dataclass
class TrustScoreResult:
    """
    Final trust score.
    """

    score: float

    authority_score: float
    freshness_score: float

    cross_check_score: float
    consistency_score: float


# =========================================================
# FINAL ANSWER
# =========================================================

@dataclass
class AnswerResult:
    """
    Final answer object returned by VRA.
    """

    # -----------------------------------------------------
    # Core Answer
    # -----------------------------------------------------

    answer: str

    trust_score: float

    confidence_score: float = 0.0
    agreement_score: float = 0.0

    # -----------------------------------------------------
    # Quality
    # -----------------------------------------------------

    answer_quality_score: float = 0.0

    answer_quality_level: str = "unknown"

    # -----------------------------------------------------
    # Safety
    # -----------------------------------------------------

    safety_score: float = 0.0

    safety_level: str = "unknown"

    matched_safety_keywords: List[str] = field(
        default_factory=list
    )

    # -----------------------------------------------------
    # Hallucination
    # -----------------------------------------------------

    hallucination_risk_score: float = 0.0

    hallucination_risk_level: str = "unknown"

    # -----------------------------------------------------
    # Consensus
    # -----------------------------------------------------

    consensus_status: str = "unknown"

    claim_count: int = 0

    unique_claim_count: int = 0

    # -----------------------------------------------------
    # Verification
    # -----------------------------------------------------

    answer_type: str = "unverified_answer"

    verification_status: str = "unverified"

    verification_badge: str = "❌ Unverified"

    verification_summary: str = ""

    # -----------------------------------------------------
    # Sources
    # -----------------------------------------------------

    source_count: int = 0

    verified_source_count: int = 0

    failed_source_count: int = 0

    sources: List[SourceInfo] = field(
        default_factory=list
    )

    # -----------------------------------------------------
    # New UI Source Cards
    # -----------------------------------------------------

    source_cards: List[Dict[str, Any]] = field(
        default_factory=list
    )

    # -----------------------------------------------------
    # Citations
    # -----------------------------------------------------

    citations: List[Dict[str, Any]] = field(
        default_factory=list
    )

    # -----------------------------------------------------
    # Evidence Summary
    # -----------------------------------------------------

    evidence_summary: List[Dict[str, Any]] = field(
        default_factory=list
    )

    evidence_graph: List[Dict[str, Any]] = field(
        default_factory=list
    )

    claim_lineage: List[Dict[str, Any]] = field(
        default_factory=list
    )

    ranked_sources: List[Dict[str, Any]] = field(
        default_factory=list
    )

    # -----------------------------------------------------
    # Advanced Verification
    # -----------------------------------------------------

    claim_groups: List[Dict[str, Any]] = field(
        default_factory=list
    )

    contradiction_result: Dict[str, Any] = field(
        default_factory=dict
    )

    evidence_clusters: List[Dict[str, Any]] = field(
        default_factory=list
    )

    multi_hop_chains: List[Dict[str, Any]] = field(
        default_factory=list
    )

    # -----------------------------------------------------
    # Raw Evidence
    # -----------------------------------------------------

    evidence_records: List[Dict[str, Any]] = field(
        default_factory=list
    )

    verified_sources: List[Dict[str, Any]] = field(
        default_factory=list
    )

    failed_sources: List[Dict[str, Any]] = field(
        default_factory=list
    )

    # -----------------------------------------------------
    # Query Understanding
    # -----------------------------------------------------

    query_intent: str = "general_factual"

    answer_mode: str = "verified_search"

    # verified_search
    # personal_assistant
    # mixed_mode

    # -----------------------------------------------------
    # Frontend Messages
    # -----------------------------------------------------

    warning_message: Optional[str] = None

    # -----------------------------------------------------
    # Personal Queries
    # -----------------------------------------------------

    is_personal_response: bool = False

    used_ai_reasoning: bool = False

    # -----------------------------------------------------
    # Metadata
    # -----------------------------------------------------

    metadata: Dict[str, Any] = field(
        default_factory=dict
    )