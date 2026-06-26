"""
=========================================================
MODULE: Dynamic Source Builder

Project:
Authentic AI Search

Purpose:
Convert raw search results into intelligent VRA-compatible
dynamic source objects.

Version:
3.0.0
=========================================================
"""

import re
from typing import Any, Dict, List
from urllib.parse import urlparse


class DynamicSourceBuilder:
    """
    Source Intelligence Layer for VRA.

    This module does not hardcode user queries.
    It ranks every discovered URL using:
    - domain authority
    - source category
    - query relevance
    - query coverage
    - content quality signal
    - freshness signal from title/snippet
    - consensus potential
    - intent-aware source boosting
    """

    HIGH_AUTHORITY_DOMAINS = {
        "who.int": 100.0,
        "nih.gov": 100.0,
        "nimh.nih.gov": 100.0,
        "cdc.gov": 100.0,
        "federalreserve.gov": 99.0,
        "worldbank.org": 99.0,
        "imf.org": 99.0,
        "un.org": 98.0,
        "rbi.org.in": 98.0,
        "mospi.gov.in": 98.0,
        "censusindia.gov.in": 98.0,
        "pmindia.gov.in": 98.0,
        "ecb.europa.eu": 98.0,
        "nhs.uk": 97.0,
        "oecd.org": 97.0,
        "isro.gov.in": 97.0,
        "sebi.gov.in": 97.0,
        "nasa.gov": 96.0,
        "bea.gov": 96.0,
        "openai.com": 95.0,
        "mayoclinic.org": 94.0,
        "britannica.com": 82.0,
        "investopedia.com": 78.0,
        "en.wikipedia.org": 75.0,
        "wikipedia.org": 75.0,
    }

    COMMUNITY_DOMAINS = {
        "reddit.com",
        "quora.com",
        "stackoverflow.com",
        "news.ycombinator.com",
        "hackernews.com",
    }

    SOCIAL_DOMAINS = {
        "x.com",
        "twitter.com",
        "facebook.com",
        "instagram.com",
        "youtube.com",
        "tiktok.com",
        "pinterest.com",
        "linkedin.com",
    }

    LOW_QUALITY_DOMAINS = {
        "bookmark4you.com",
        "wikimili.com",
        "ipaddress.com",
        "knittystash.com",
        "grokipedia.com",
    }

    REFERENCE_DOMAINS = {
        "wikipedia.org",
        "en.wikipedia.org",
        "britannica.com",
        "investopedia.com",
    }

    OPINION_INTENT_TERMS = {
        "opinion",
        "review",
        "reviews",
        "experience",
        "experiences",
        "people think",
        "users think",
        "community",
        "reddit",
        "discussion",
        "feedback",
        "complaints",
    }

    HEALTH_SUPPORT_TERMS = {
        "not feeling good",
        "feel sad",
        "sad",
        "depressed",
        "anxiety",
        "anxious",
        "panic",
        "mental health",
        "stress",
        "stressed",
        "suicide",
        "self harm",
        "help me",
    }

    CURRENT_INFO_TERMS = {
        "current",
        "latest",
        "today",
        "now",
        "rate",
        "price",
        "population",
        "gdp",
        "inflation",
        "news",
        "update",
        "2024",
        "2025",
        "2026",
    }

    def _normalize_text(self, text: str) -> str:
        return " ".join(
            text.lower()
            .replace("?", " ")
            .replace(",", " ")
            .replace(".", " ")
            .replace("!", " ")
            .replace(":", " ")
            .replace(";", " ")
            .split()
        )

    def _domain_from_url(self, url: str) -> str:
        parsed_url = urlparse(url)

        return (
            parsed_url.netloc
            .replace("www.", "")
            .lower()
            .strip()
        )

    def _is_subdomain_of(
        self,
        domain: str,
        parent_domain: str
    ) -> bool:
        return (
            domain == parent_domain
            or domain.endswith(f".{parent_domain}")
        )

    def _known_domain_score(self, domain: str) -> float | None:
        if domain in self.HIGH_AUTHORITY_DOMAINS:
            return self.HIGH_AUTHORITY_DOMAINS[domain]

        for known_domain, score in self.HIGH_AUTHORITY_DOMAINS.items():
            if self._is_subdomain_of(domain, known_domain):
                return score

        return None

    def _source_category(self, domain: str) -> str:
        if self._known_domain_score(domain) is not None:
            if domain.endswith(".gov") or domain.endswith(".gov.in"):
                return "official_government"

            if domain.endswith(".int"):
                return "official_international"

            if domain.endswith(".edu") or domain.endswith(".ac.in"):
                return "academic"

            if domain in self.REFERENCE_DOMAINS:
                return "reference"

            return "trusted_institution"

        if domain.endswith(".gov") or domain.endswith(".gov.in"):
            return "official_government"

        if domain.endswith(".edu") or domain.endswith(".ac.in"):
            return "academic"

        if domain.endswith(".int"):
            return "official_international"

        if domain in self.COMMUNITY_DOMAINS:
            return "community"

        if domain in self.SOCIAL_DOMAINS:
            return "social"

        if domain in self.LOW_QUALITY_DOMAINS:
            return "low_quality"

        if "wikipedia.org" in domain:
            return "reference"

        if domain.endswith(".org"):
            return "organization"

        return "web"

    def _trust_tier(
        self,
        category: str,
        authority_score: float
    ) -> str:
        if authority_score >= 95:
            return "tier_1"

        if authority_score >= 85:
            return "tier_2"

        if authority_score >= 70:
            return "tier_3"

        if authority_score >= 50:
            return "tier_4"

        return "tier_5"

    def _authority_score(self, domain: str) -> float:
        known_score = self._known_domain_score(domain)

        if known_score is not None:
            return known_score

        category = self._source_category(domain)

        category_scores = {
            "official_government": 96.0,
            "official_international": 94.0,
            "academic": 90.0,
            "trusted_institution": 88.0,
            "reference": 75.0,
            "organization": 72.0,
            "community": 55.0,
            "web": 50.0,
            "social": 35.0,
            "low_quality": 25.0,
        }

        return category_scores.get(category, 50.0)

    def _source_type(
        self,
        category: str
    ) -> str:
        if category in {
            "official_government",
            "official_international",
            "academic",
            "trusted_institution",
        }:
            return "official_organization"

        if category in {
            "reference",
            "organization",
        }:
            return "reference"

        if category == "community":
            return "community"

        if category == "social":
            return "social"

        if category == "low_quality":
            return "low_quality"

        return "web"

    def _query_terms(
        self,
        query_text: str
    ) -> List[str]:
        normalized_query = self._normalize_text(query_text)

        stop_words = {
            "what",
            "which",
            "when",
            "where",
            "why",
            "how",
            "who",
            "is",
            "are",
            "was",
            "were",
            "the",
            "a",
            "an",
            "of",
            "in",
            "on",
            "for",
            "to",
            "and",
            "or",
            "me",
            "tell",
            "explain",
            "about",
        }

        return [
            word
            for word in normalized_query.split()
            if len(word) > 2 and word not in stop_words
        ]

    def _detect_query_intent(
        self,
        query_text: str
    ) -> str:
        query_lower = query_text.lower()

        if any(term in query_lower for term in self.HEALTH_SUPPORT_TERMS):
            return "health_support"

        if any(term in query_lower for term in self.OPINION_INTENT_TERMS):
            return "community_opinion"

        if any(term in query_lower for term in self.CURRENT_INFO_TERMS):
            return "current_factual"

        return "general_factual"

    def _relevance_score(
        self,
        query_text: str,
        title: str,
        snippet: str,
        domain: str
    ) -> float:
        terms = self._query_terms(query_text)

        if not terms:
            return 50.0

        combined_text = self._normalize_text(
            f"{title} {snippet} {domain}"
        )

        matched_terms = [
            term
            for term in terms
            if term in combined_text
        ]

        exact_phrase_bonus = 0.0

        normalized_query = self._normalize_text(query_text)

        if normalized_query and normalized_query in combined_text:
            exact_phrase_bonus = 25.0

        base_score = (
            len(matched_terms) / len(terms)
        ) * 75.0

        return round(
            min(base_score + exact_phrase_bonus, 100.0),
            2
        )

    def _coverage_score(
        self,
        query_text: str,
        title: str,
        snippet: str
    ) -> float:
        terms = self._query_terms(query_text)

        if not terms:
            return 50.0

        combined_text = self._normalize_text(
            f"{title} {snippet}"
        )

        covered_terms = set()

        for term in terms:
            if term in combined_text:
                covered_terms.add(term)

        return round(
            (len(covered_terms) / len(terms)) * 100.0,
            2
        )

    def _content_quality_score(
        self,
        title: str,
        snippet: str,
        category: str
    ) -> float:
        combined_text = self._normalize_text(
            f"{title} {snippet}"
        )

        score = 50.0

        positive_markers = {
            "official",
            "about",
            "definition",
            "explained",
            "report",
            "data",
            "statistics",
            "research",
            "guidance",
            "faq",
            "profile",
            "biography",
            "overview",
        }

        negative_markers = {
            "login",
            "sign up",
            "coupon",
            "download app",
            "viral",
            "rumor",
            "gossip",
            "ads",
            "sponsored",
        }

        for marker in positive_markers:
            if marker in combined_text:
                score += 5.0

        for marker in negative_markers:
            if marker in combined_text:
                score -= 10.0

        if category in {
            "official_government",
            "official_international",
            "academic",
            "trusted_institution",
        }:
            score += 15.0

        if category in {
            "social",
            "low_quality",
        }:
            score -= 20.0

        return round(
            max(0.0, min(score, 100.0)),
            2
        )

    def _freshness_signal_score(
        self,
        title: str,
        snippet: str
    ) -> float:
        combined_text = f"{title} {snippet}".lower()

        year_matches = re.findall(
            r"\b(20[1-3][0-9])\b",
            combined_text
        )

        if not year_matches:
            return 50.0

        years = [
            int(year)
            for year in year_matches
        ]

        latest_year = max(years)

        if latest_year >= 2025:
            return 90.0

        if latest_year >= 2023:
            return 75.0

        if latest_year >= 2020:
            return 60.0

        return 40.0

    def _intent_boost(
        self,
        intent: str,
        category: str
    ) -> float:
        if intent == "health_support":
            if category in {
                "official_government",
                "official_international",
                "academic",
                "trusted_institution",
            }:
                return 20.0

            if category in {
                "community",
                "social",
                "low_quality",
            }:
                return -25.0

        if intent == "community_opinion":
            if category in {
                "community",
                "social",
            }:
                return 20.0

            if category in {
                "official_government",
                "official_international",
                "academic",
            }:
                return -5.0

        if intent == "current_factual":
            if category in {
                "official_government",
                "official_international",
                "academic",
                "trusted_institution",
            }:
                return 15.0

        if intent == "general_factual":
            if category in {
                "official_government",
                "official_international",
                "academic",
                "trusted_institution",
                "reference",
            }:
                return 10.0

        return 0.0

    def _consensus_potential_score(
        self,
        domain: str,
        category: str,
        same_category_count: int
    ) -> float:
        base_score = min(
            same_category_count * 10.0,
            60.0
        )

        if category in {
            "official_government",
            "official_international",
            "academic",
            "trusted_institution",
        }:
            base_score += 25.0

        if category in {
            "community",
            "social",
        }:
            base_score += 5.0

        if category == "low_quality":
            base_score -= 25.0

        return round(
            max(0.0, min(base_score, 100.0)),
            2
        )

    def _final_discovery_score(
        self,
        authority_score: float,
        relevance_score: float,
        coverage_score: float,
        content_quality_score: float,
        freshness_score: float,
        consensus_potential_score: float,
        intent_boost: float
    ) -> float:
        score = (
            authority_score * 0.30
            + relevance_score * 0.25
            + coverage_score * 0.15
            + content_quality_score * 0.10
            + freshness_score * 0.08
            + consensus_potential_score * 0.12
            + intent_boost
        )

        return round(
            max(0.0, min(score, 100.0)),
            2
        )

    def _source_quality_level(
        self,
        discovery_score: float
    ) -> str:
        if discovery_score >= 90:
            return "excellent"

        if discovery_score >= 80:
            return "very_good"

        if discovery_score >= 70:
            return "good"

        if discovery_score >= 55:
            return "usable"

        return "weak"

    def build_sources(
        self,
        search_results: List[Dict[str, Any]],
        query_text: str = "",
    ) -> List[Dict[str, Any]]:
        """
        Build ranked VRA-compatible dynamic sources.
        """

        intent = self._detect_query_intent(query_text)

        category_counts: Dict[str, int] = {}

        normalized_candidates = []

        seen_urls = set()

        for result in search_results:
            url = result.get("url", "")

            if not url or url in seen_urls:
                continue

            domain = (
                result.get("domain")
                or self._domain_from_url(url)
            )

            if not domain:
                continue

            category = self._source_category(domain)

            category_counts[category] = (
                category_counts.get(category, 0) + 1
            )

            normalized_candidates.append(
                {
                    "result": result,
                    "domain": domain,
                    "category": category,
                }
            )

            seen_urls.add(url)

        sources: List[Dict[str, Any]] = []

        for index, candidate in enumerate(
            normalized_candidates,
            start=1
        ):
            result = candidate["result"]
            domain = candidate["domain"]
            category = candidate["category"]

            url = result.get("url", "")
            title = result.get("title", "")
            snippet = result.get("snippet", "")

            authority_score = self._authority_score(domain)

            relevance_score = self._relevance_score(
                query_text=query_text,
                title=title,
                snippet=snippet,
                domain=domain
            )

            coverage_score = self._coverage_score(
                query_text=query_text,
                title=title,
                snippet=snippet
            )

            content_quality_score = self._content_quality_score(
                title=title,
                snippet=snippet,
                category=category
            )

            freshness_signal_score = self._freshness_signal_score(
                title=title,
                snippet=snippet
            )

            consensus_potential_score = self._consensus_potential_score(
                domain=domain,
                category=category,
                same_category_count=category_counts.get(category, 1)
            )

            intent_boost = self._intent_boost(
                intent=intent,
                category=category
            )

            discovery_score = self._final_discovery_score(
                authority_score=authority_score,
                relevance_score=relevance_score,
                coverage_score=coverage_score,
                content_quality_score=content_quality_score,
                freshness_score=freshness_signal_score,
                consensus_potential_score=consensus_potential_score,
                intent_boost=intent_boost
            )

            trust_tier = self._trust_tier(
                category=category,
                authority_score=authority_score
            )

            sources.append(
                {
                    "id": f"dynamic_{index}_{domain}",
                    "name": title or domain,
                    "domain": domain,
                    "base_url": url,
                    "source_type": self._source_type(category),
                    "source_category": category,
                    "trust_tier": trust_tier,
                    "authority_score": authority_score,
                    "relevance_score": relevance_score,
                    "coverage_score": coverage_score,
                    "content_quality_score": content_quality_score,
                    "freshness_signal_score": freshness_signal_score,
                    "consensus_potential_score": consensus_potential_score,
                    "intent_boost": intent_boost,
                    "discovery_score": discovery_score,
                    "source_quality_level": self._source_quality_level(
                        discovery_score
                    ),
                    "is_official": category in {
                        "official_government",
                        "official_international",
                        "academic",
                        "trusted_institution",
                    },
                    "api_available": False,
                    "update_frequency": "unknown",
                    "status": "active",
                    "notes": snippet,
                    "registry_category": "dynamic_search",
                    "dynamic": True,
                    "query_intent": intent,
                    "search_query": result.get("search_query"),
                    "search_backend": result.get("search_backend"),
                }
            )

        return sorted(
            sources,
            key=lambda source: (
                source.get("discovery_score", 0),
                source.get("authority_score", 0),
                source.get("relevance_score", 0),
                source.get("content_quality_score", 0),
            ),
            reverse=True
        )