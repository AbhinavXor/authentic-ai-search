"""
=========================================================
MODULE: Source Discovery Ranker

Project:
Authentic AI Search

Purpose:
Rank dynamically discovered sources for VRA.

Version:
2.1.0
=========================================================
"""

from typing import Any, Dict, List


class SourceDiscoveryRanker:
    """
    Ranks dynamic sources using source intelligence fields created by
    DynamicSourceBuilder.

    Ranking goals:
    - Official/authentic sources first for factual queries.
    - Entity/person queries prefer profile, biography, official, reference,
      and reputable institutional pages.
    - Health/support queries prefer medical/government/institutional sources.
    - Opinion/community queries allow community/social sources but still keep
      trusted institutional context nearby.
    - Keep domain diversity.
    """

    FACTUAL_INTENTS = {
        "general_factual",
        "current_factual",
        "health_support",
    }

    COMMUNITY_INTENTS = {
        "community_opinion",
    }

    ENTITY_QUERY_PREFIXES = (
        "who is",
        "who was",
    )

    ENTITY_PAGE_HINTS = {
        "profile",
        "biography",
        "bio",
        "about",
        "official",
        "prime minister",
        "president",
        "founder",
        "ceo",
        "chief executive",
        "member of parliament",
        "minister",
        "career",
        "early life",
    }

    ENTITY_BAD_HINTS = {
        "latest news",
        "breaking news",
        "video",
        "photos",
        "instagram",
        "facebook",
        "youtube",
        "tiktok",
        "pinterest",
        "x.com",
        "twitter",
        "login",
        "sign in",
        "download",
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

    def _combined_text(
        self,
        source: Dict[str, Any]
    ) -> str:
        return " ".join(
            str(source.get(field, "") or "")
            for field in [
                "name",
                "title",
                "domain",
                "base_url",
                "url",
                "notes",
                "snippet",
                "source_category",
                "source_type",
            ]
        ).lower()

    def _query_text(
        self,
        source: Dict[str, Any]
    ) -> str:
        return str(
            source.get("query")
            or source.get("query_text")
            or source.get("search_query")
            or ""
        ).lower().strip()

    def _is_entity_query(
        self,
        source: Dict[str, Any]
    ) -> bool:
        query_text = self._query_text(source)

        return query_text.startswith(
            self.ENTITY_QUERY_PREFIXES
        )

    def _domain_limit_for_intent(
        self,
        intent: str
    ) -> int:
        if intent == "community_opinion":
            return 3

        return 1

    def _intent_adjustment(
        self,
        source: Dict[str, Any]
    ) -> float:
        intent = source.get("query_intent", "general_factual")
        category = source.get("source_category", "web")

        if intent in self.FACTUAL_INTENTS:
            if category in {
                "official_government",
                "official_international",
                "academic",
                "trusted_institution",
                "reference",
            }:
                return 12.0

            if category in {
                "community",
                "social",
                "low_quality",
            }:
                return -18.0

        if intent == "community_opinion":
            if category in {
                "community",
                "social",
            }:
                return 12.0

            if category in {
                "academic",
                "trusted_institution",
                "reference",
            }:
                return 6.0

            if category in {
                "official_government",
                "official_international",
            }:
                return 2.0

        return 0.0

    def _entity_adjustment(
        self,
        source: Dict[str, Any]
    ) -> float:
        if not self._is_entity_query(source):
            return 0.0

        text = self._combined_text(source)
        category = source.get("source_category", "web")
        domain = str(source.get("domain", "") or "").lower()

        score = 0.0

        if category in {
            "official_government",
            "official_international",
            "trusted_institution",
            "reference",
            "academic",
        }:
            score += 10.0

        if any(hint in text for hint in self.ENTITY_PAGE_HINTS):
            score += 16.0

        if any(hint in text for hint in self.ENTITY_BAD_HINTS):
            score -= 18.0

        if domain in {
            "instagram.com",
            "facebook.com",
            "youtube.com",
            "tiktok.com",
            "pinterest.com",
            "x.com",
            "twitter.com",
        }:
            score -= 25.0

        # For entity identity queries, exact official/reference pages
        # are usually better than broad news pages.
        if category == "web" and "news" in text:
            score -= 8.0

        return score

    def _quality_adjustment(
        self,
        source: Dict[str, Any]
    ) -> float:
        quality = source.get("source_quality_level", "weak")

        quality_boosts = {
            "excellent": 10.0,
            "very_good": 7.0,
            "good": 4.0,
            "usable": 0.0,
            "weak": -8.0,
        }

        return quality_boosts.get(quality, 0.0)

    def _trust_tier_adjustment(
        self,
        source: Dict[str, Any]
    ) -> float:
        tier = source.get("trust_tier", "tier_5")

        tier_boosts = {
            "tier_1": 10.0,
            "tier_2": 7.0,
            "tier_3": 4.0,
            "tier_4": 0.0,
            "tier_5": -8.0,
        }

        return tier_boosts.get(tier, 0.0)

    def _final_rank_score(
        self,
        source: Dict[str, Any]
    ) -> float:
        discovery_score = self._safe_float(
            source.get("discovery_score"),
            0.0
        )

        authority_score = self._safe_float(
            source.get("authority_score"),
            0.0
        )

        relevance_score = self._safe_float(
            source.get("relevance_score"),
            0.0
        )

        content_quality_score = self._safe_float(
            source.get("content_quality_score"),
            0.0
        )

        rank_score = (
            discovery_score * 0.42
            + authority_score * 0.25
            + relevance_score * 0.18
            + content_quality_score * 0.15
            + self._intent_adjustment(source)
            + self._entity_adjustment(source)
            + self._quality_adjustment(source)
            + self._trust_tier_adjustment(source)
        )

        return round(
            max(0.0, min(rank_score, 100.0)),
            2
        )

    def rank(
        self,
        sources: List[Dict[str, Any]],
        max_sources: int | None = None
    ) -> List[Dict[str, Any]]:
        if not sources:
            return []

        ranked_sources = []

        for source in sources:
            enriched_source = dict(source)
            enriched_source["rank_score"] = self._final_rank_score(source)
            ranked_sources.append(enriched_source)

        ranked_sources = sorted(
            ranked_sources,
            key=lambda source: (
                source.get("rank_score", 0),
                source.get("authority_score", 0),
                source.get("relevance_score", 0),
            ),
            reverse=True
        )

        diversified_sources = []
        domain_counts: Dict[str, int] = {}

        intent = ranked_sources[0].get(
            "query_intent",
            "general_factual"
        )

        max_per_domain = self._domain_limit_for_intent(intent)

        for source in ranked_sources:
            domain = str(
                   source.get("domain", "")
            ).lower().strip()

            if not domain:
                continue

            current_count = domain_counts.get(domain, 0)

            if current_count >= max_per_domain:
                continue

            diversified_sources.append(source)
            domain_counts[domain] = current_count + 1

            if max_sources and len(diversified_sources) >= max_sources:
                break

        return diversified_sources