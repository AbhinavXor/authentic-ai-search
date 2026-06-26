"""
=========================================================
MODULE: Official Source Detector

Project:
Authentic AI Search

Purpose:
Detect, classify, and score official / trusted / community /
social / low-quality sources for dynamic VRA search.

Version:
3.0.0
=========================================================
"""

from typing import Any, Dict, List
from urllib.parse import urlparse


class OfficialSourceDetector:
    """
    Industry-style source authenticity detector.

    Design:
    - Do not hard-block sources at discovery stage.
    - Classify every source.
    - Score authenticity dynamically.
    - Official/trusted sources rank high.
    - Social/community sources remain available for opinion queries.
    - Low-quality/spam-like sources rank very low.
    """

    EXACT_TIER_1_DOMAINS = {
        # Global / international
        "who.int",
        "un.org",
        "worldbank.org",
        "imf.org",
        "oecd.org",
        "wto.org",
        "ilo.org",
        "unesco.org",
        "unicef.org",
        "fao.org",

        # India official
        "india.gov.in",
        "data.gov.in",
        "rbi.org.in",
        "mospi.gov.in",
        "censusindia.gov.in",
        "pmindia.gov.in",
        "isro.gov.in",
        "sebi.gov.in",
        "eci.gov.in",
        "uidai.gov.in",
        "incometax.gov.in",
        "meity.gov.in",
        "mohfw.gov.in",
        "mha.gov.in",
        "mea.gov.in",
        "finmin.gov.in",

        # US / economy / statistics
        "federalreserve.gov",
        "bea.gov",
        "bls.gov",
        "census.gov",
        "treasury.gov",
        "congress.gov",
        "commerce.gov",
        "sec.gov",
        "cdc.gov",
        "nih.gov",
        "nimh.nih.gov",
        "nasa.gov",

        # Europe / UK
        "ecb.europa.eu",
        "europa.eu",
        "gov.uk",
        "ons.gov.uk",
        "nhs.uk",
        "bankofengland.co.uk",
    }

    EXACT_TIER_2_DOMAINS = {
        # Medical / health
        "mayoclinic.org",
        "clevelandclinic.org",
        "hopkinsmedicine.org",
        "medlineplus.gov",
        "healthline.com",
        "webmd.com",

        # Academic / research publishers
        "nature.com",
        "science.org",
        "thelancet.com",
        "nejm.org",
        "pubmed.ncbi.nlm.nih.gov",
        "ncbi.nlm.nih.gov",
        "arxiv.org",
        "ssrn.com",

        # Universities / think tanks
        "harvard.edu",
        "stanford.edu",
        "mit.edu",
        "berkeley.edu",
        "ox.ac.uk",
        "cam.ac.uk",
        "brookings.edu",

        # Reference
        "britannica.com",
        "investopedia.com",
        "wikipedia.org",
        "en.wikipedia.org",
    }

    COMMUNITY_DOMAINS = {
        "reddit.com",
        "quora.com",
        "stackoverflow.com",
        "stackexchange.com",
        "news.ycombinator.com",
        "hackernews.com",
    }

    SOCIAL_DOMAINS = {
        "x.com",
        "twitter.com",
        "facebook.com",
        "instagram.com",
        "youtube.com",
        "youtu.be",
        "tiktok.com",
        "pinterest.com",
        "linkedin.com",
        "threads.net",
        "snapchat.com",
    }

    LOW_QUALITY_SIGNALS = {
        "bookmark",
        "coupon",
        "free-download",
        "apk",
        "pirated",
        "torrent",
        "gossip",
        "viral",
        "rumor",
        "rumour",
        "clickbait",
        "wallpaper",
        "lyrics",
        "astrology",
        "prophet",
        "unknownfacts",
    }

    EXACT_LOW_QUALITY_DOMAINS = {
        "bookmark4you.com",
        "wikimili.com",
        "ipaddress.com",
        "knittystash.com",
        "grokipedia.com",
    }

    NEWS_HINT_DOMAINS = {
        "reuters.com",
        "apnews.com",
        "bbc.com",
        "bbc.co.uk",
        "theguardian.com",
        "nytimes.com",
        "washingtonpost.com",
        "economist.com",
        "ft.com",
        "bloomberg.com",
        "wsj.com",
        "thehindu.com",
        "indianexpress.com",
        "hindustantimes.com",
        "business-standard.com",
        "livemint.com",
    }

    def _normalize_domain(self, domain_or_url: str) -> str:
        value = (domain_or_url or "").strip().lower()

        if not value:
            return ""

        if value.startswith("http://") or value.startswith("https://"):
            parsed = urlparse(value)
            value = parsed.netloc

        if value.startswith("www."):
            value = value[4:]

        return value.strip("/")

    def _is_subdomain_of(self, domain: str, parent_domain: str) -> bool:
        return domain == parent_domain or domain.endswith(f".{parent_domain}")

    def _matches_any(self, domain: str, domains: set[str]) -> bool:
        return any(
            self._is_subdomain_of(domain, known_domain)
            for known_domain in domains
        )

    def _has_low_quality_signal(self, domain: str) -> bool:
        return any(signal in domain for signal in self.LOW_QUALITY_SIGNALS)

    def source_authenticity_category(self, domain: str) -> str:
        domain = self._normalize_domain(domain)

        if not domain:
            return "unknown"

        if self._matches_any(domain, self.EXACT_LOW_QUALITY_DOMAINS):
            return "low_quality_source"

        if self._has_low_quality_signal(domain):
            return "low_quality_source"

        if self._matches_any(domain, self.EXACT_TIER_1_DOMAINS):
            return "official_verified"

        if domain.endswith(".gov") or ".gov." in domain:
            return "official_government"

        if domain.endswith(".gov.in"):
            return "official_government"

        if domain.endswith(".int"):
            return "official_international"

        if domain.endswith(".edu") or domain.endswith(".ac.in") or ".edu." in domain:
            return "academic_institution"

        if domain.endswith(".europa.eu"):
            return "official_international"

        if self._matches_any(domain, self.EXACT_TIER_2_DOMAINS):
            return "trusted_reference"

        if self._matches_any(domain, self.NEWS_HINT_DOMAINS):
            return "reputable_news"

        if self._matches_any(domain, self.COMMUNITY_DOMAINS):
            return "community_source"

        if self._matches_any(domain, self.SOCIAL_DOMAINS):
            return "social_source"

        if domain.endswith(".org"):
            return "organization_source"

        return "general_web_source"

    def official_confidence_score(self, domain: str) -> float:
        category = self.source_authenticity_category(domain)

        scores = {
            "official_verified": 100.0,
            "official_government": 97.0,
            "official_international": 96.0,
            "academic_institution": 92.0,
            "trusted_reference": 86.0,
            "reputable_news": 78.0,
            "organization_source": 70.0,
            "community_source": 55.0,
            "general_web_source": 50.0,
            "social_source": 35.0,
            "low_quality_source": 15.0,
            "unknown": 0.0,
        }

        return scores.get(category, 50.0)

    def is_official_domain(self, domain: str) -> bool:
        category = self.source_authenticity_category(domain)

        return category in {
            "official_verified",
            "official_government",
            "official_international",
            "academic_institution",
        }

    def is_trusted_domain(self, domain: str) -> bool:
        category = self.source_authenticity_category(domain)

        return category in {
            "official_verified",
            "official_government",
            "official_international",
            "academic_institution",
            "trusted_reference",
            "reputable_news",
        }

    def should_use_for_verified_answer(self, domain: str) -> bool:
        """
        True means this source can support a verified factual answer.
        Community/social sources are not rejected globally, but they should
        not normally create a verified factual badge.
        """

        category = self.source_authenticity_category(domain)

        return category in {
            "official_verified",
            "official_government",
            "official_international",
            "academic_institution",
            "trusted_reference",
            "reputable_news",
            "organization_source",
        }

    def source_risk_level(self, domain: str) -> str:
        score = self.official_confidence_score(domain)

        if score >= 90:
            return "very_low_risk"

        if score >= 75:
            return "low_risk"

        if score >= 55:
            return "medium_risk"

        if score >= 35:
            return "high_risk"

        return "very_high_risk"

    def enrich_source(self, source: Dict[str, Any]) -> Dict[str, Any]:
        enriched = dict(source)

        domain = self._normalize_domain(
            enriched.get("domain") or enriched.get("base_url") or enriched.get("url", "")
        )

        category = self.source_authenticity_category(domain)
        official_confidence = self.official_confidence_score(domain)

        existing_authority = float(enriched.get("authority_score", 0) or 0)

        enriched["domain"] = domain
        enriched["authenticity_category"] = category
        enriched["official_confidence_score"] = official_confidence
        enriched["source_risk_level"] = self.source_risk_level(domain)
        enriched["is_official"] = self.is_official_domain(domain)
        enriched["is_trusted"] = self.is_trusted_domain(domain)
        enriched["can_support_verified_answer"] = self.should_use_for_verified_answer(domain)
        enriched["authority_score"] = max(existing_authority, official_confidence)

        return enriched

    def enrich_sources(self, sources: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        return [self.enrich_source(source) for source in sources]

    def filter_official_sources(self, sources: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Backward-compatible method.

        Later pipeline should prefer enrich_sources(), not this hard filter.
        """

        return [
            enriched
            for enriched in self.enrich_sources(sources)
            if enriched.get("is_official")
        ]

    def filter_trusted_sources(self, sources: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        return [
            enriched
            for enriched in self.enrich_sources(sources)
            if enriched.get("is_trusted")
        ]

    def filter_verified_answer_sources(
        self,
        sources: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        return [
            enriched
            for enriched in self.enrich_sources(sources)
            if enriched.get("can_support_verified_answer")
        ]