"""
=========================================================
MODULE: Source Ranking Model

Project:
Authentic AI Search

Purpose:
Rank fetched evidence sources using VRA trust signals.

Version:
2.0.0
=========================================================
"""

from typing import Any, Dict, List


class SourceRankingModel:
    """
    Industry-grade source ranking model.

    Uses:
    - authority score
    - official confidence
    - query relevance
    - content quality
    - freshness
    - trust tier
    - source risk
    - query intent
    - verified-answer eligibility
    """

    FACTUAL_INTENTS = {
        "general_factual",
        "current_factual",
        "health_support",
    }

    COMMUNITY_INTENTS = {
        "community_opinion",
    }

    TRUST_TIER_SCORES = {
        "tier_1": 100.0,
        "tier_2": 85.0,
        "tier_3": 72.0,
        "tier_4": 55.0,
        "tier_5": 35.0,
        "tier_a_verified": 100.0,
        "tier_b_trusted": 85.0,
        "tier_c_reference": 72.0,
        "tier_d_community": 55.0,
        "tier_e_social": 35.0,
    }

    RISK_PENALTIES = {
        "very_low_risk": 0.0,
        "low_risk": 3.0,
        "medium_risk": 10.0,
        "high_risk": 25.0,
        "very_high_risk": 45.0,
    }

    CATEGORY_BASE_SCORES = {
        "official_verified": 100.0,
        "official_government": 97.0,
        "official_international": 96.0,
        "academic_institution": 92.0,
        "trusted_reference": 86.0,
        "reputable_news": 78.0,
        "official_organization": 92.0,
        "trusted_institution": 88.0,
        "reference": 75.0,
        "organization_source": 70.0,
        "community_source": 55.0,
        "community": 55.0,
        "general_web_source": 50.0,
        "web": 50.0,
        "social_source": 35.0,
        "social": 35.0,
        "low_quality_source": 15.0,
        "low_quality": 15.0,
    }

    def _safe_float(
        self,
        value: Any,
        default: float = 0.0
    ) -> float:
        try:
            if value is None:
                return default

            return float(value)

        except Exception:
            return default

    def _query_intent(
        self,
        record: Dict[str, Any]
    ) -> str:
        return (
            record.get("query_intent")
            or record.get("intent")
            or "general_factual"
        )

    def _source_category(
        self,
        record: Dict[str, Any]
    ) -> str:
        return (
            record.get("authenticity_category")
            or record.get("source_category")
            or record.get("source_type")
            or "web"
        )

    def _trust_tier_score(
        self,
        record: Dict[str, Any]
    ) -> float:
        tier = record.get("trust_tier", "")

        return self.TRUST_TIER_SCORES.get(
            tier,
            50.0
        )

    def _category_score(
        self,
        record: Dict[str, Any]
    ) -> float:
        category = self._source_category(record)

        return self.CATEGORY_BASE_SCORES.get(
            category,
            50.0
        )

    def _freshness_score(
        self,
        record: Dict[str, Any]
    ) -> float:
        return self._safe_float(
            record.get("freshness_score")
            or record.get("freshness_signal_score"),
            50.0
        )

    def _intent_adjustment(
        self,
        record: Dict[str, Any]
    ) -> float:
        intent = self._query_intent(record)
        category = self._source_category(record)

        if intent == "health_support":
            if category in {
                "official_verified",
                "official_government",
                "official_international",
                "academic_institution",
                "trusted_reference",
                "trusted_institution",
                "official_organization",
            }:
                return 15.0

            if category in {
                "community_source",
                "community",
                "social_source",
                "social",
                "low_quality_source",
                "low_quality",
            }:
                return -30.0

        if intent == "community_opinion":
            if category in {
                "community_source",
                "community",
                "social_source",
                "social",
            }:
                return 18.0

            if category in {
                "trusted_reference",
                "academic_institution",
                "trusted_institution",
                "reference",
            }:
                return 8.0

            if category in {
                "official_verified",
                "official_government",
                "official_international",
            }:
                return 2.0

        if intent in {
            "general_factual",
            "current_factual",
        }:
            if category in {
                "official_verified",
                "official_government",
                "official_international",
                "academic_institution",
                "trusted_reference",
                "trusted_institution",
                "official_organization",
            }:
                return 12.0

            if category in {
                "community_source",
                "community",
                "social_source",
                "social",
            }:
                return -15.0

            if category in {
                "low_quality_source",
                "low_quality",
            }:
                return -35.0

        return 0.0

    def _verified_answer_adjustment(
        self,
        record: Dict[str, Any]
    ) -> float:
        if record.get("can_support_verified_answer") is True:
            return 10.0

        if record.get("can_support_verified_answer") is False:
            return -20.0

        if record.get("is_official"):
            return 8.0

        if record.get("is_trusted"):
            return 5.0

        return 0.0

    def _risk_penalty(
        self,
        record: Dict[str, Any]
    ) -> float:
        risk_level = record.get(
            "source_risk_level",
            "medium_risk"
        )

        return self.RISK_PENALTIES.get(
            risk_level,
            10.0
        )

    def _content_presence_adjustment(
        self,
        record: Dict[str, Any]
    ) -> float:
        retrieval_status = record.get("retrieval_status")

        if retrieval_status and retrieval_status != "success":
            return -35.0

        page_text = record.get("page_text") or ""
        extracted_claim = record.get("extracted_claim") or ""

        adjustment = 0.0

        if page_text and len(page_text) >= 500:
            adjustment += 5.0

        if page_text and len(page_text) >= 1500:
            adjustment += 5.0

        if extracted_claim:
            adjustment += 8.0

        return adjustment

    def _ranking_reason(
        self,
        record: Dict[str, Any],
        score: float
    ) -> str:
        category = self._source_category(record)
        intent = self._query_intent(record)

        if record.get("is_official"):
            return (
                f"Ranked high because it is an official source "
                f"with strong authority for {intent} queries."
            )

        if record.get("is_trusted"):
            return (
                f"Ranked as trusted because it has good authenticity "
                f"and relevance for {intent} queries."
            )

        if category in {
            "community_source",
            "community",
            "social_source",
            "social",
        }:
            if intent == "community_opinion":
                return (
                    "Ranked because the query asks for community or "
                    "user opinion."
                )

            return (
                "Ranked lower because community/social sources are not "
                "primary evidence for factual verification."
            )

        if score < 50:
            return (
                "Ranked low due to weaker authority, relevance, or "
                "source quality signals."
            )

        return (
            "Ranked using authority, relevance, content quality, "
            "freshness, and trust signals."
        )

    def _rank_score(
        self,
        record: Dict[str, Any]
    ) -> float:
        authority_score = self._safe_float(
            record.get("authority_score"),
            self._category_score(record)
        )

        official_confidence_score = self._safe_float(
            record.get("official_confidence_score"),
            self._category_score(record)
        )

        relevance_score = self._safe_float(
            record.get("relevance_score"),
            50.0
        )

        content_quality_score = self._safe_float(
            record.get("content_quality_score"),
            50.0
        )

        freshness_score = self._freshness_score(record)

        trust_tier_score = self._trust_tier_score(record)

        category_score = self._category_score(record)

        score = (
            authority_score * 0.24
            + official_confidence_score * 0.22
            + relevance_score * 0.18
            + content_quality_score * 0.12
            + trust_tier_score * 0.10
            + category_score * 0.08
            + freshness_score * 0.06
        )

        score += self._intent_adjustment(record)
        score += self._verified_answer_adjustment(record)
        score += self._content_presence_adjustment(record)
        score -= self._risk_penalty(record)

        return round(
            max(0.0, min(score, 100.0)),
            2
        )

    def _rank_level(
        self,
        score: float
    ) -> str:
        if score >= 90:
            return "tier_a_verified"

        if score >= 80:
            return "tier_b_trusted"

        if score >= 70:
            return "tier_c_reference"

        if score >= 50:
            return "tier_d_usable"

        return "tier_e_weak"

    def _dedupe_key(
        self,
        record: Dict[str, Any]
    ) -> str:
        url = (
            record.get("source_url")
            or record.get("base_url")
            or record.get("url")
            or ""
        )

        if url:
            return url.strip().lower()

        return (
            record.get("domain", "")
            + "::"
            + record.get("source_name", "")
        ).lower()

    def rank(
        self,
        evidence_records: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:

        if not evidence_records:
            return []

        ranked_records: List[Dict[str, Any]] = []
        seen_keys = set()

        for record in evidence_records:
            key = self._dedupe_key(record)

            if key in seen_keys:
                continue

            seen_keys.add(key)

            enriched_record = dict(record)

            score = self._rank_score(enriched_record)

            enriched_record["source_score"] = score
            enriched_record["rank_score"] = score
            enriched_record["rank_level"] = self._rank_level(score)
            enriched_record["ranking_reason"] = self._ranking_reason(
                enriched_record,
                score
            )

            ranked_records.append(enriched_record)

        ranked_records = sorted(
            ranked_records,
            key=lambda record: (
                record.get("rank_score", 0),
                record.get("authority_score", 0),
                record.get("relevance_score", 0),
            ),
            reverse=True
        )

        for index, record in enumerate(ranked_records, start=1):
            record["source_rank"] = index

        return ranked_records