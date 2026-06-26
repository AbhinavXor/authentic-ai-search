"""
=========================================================
MODULE: Query Retriever

Project:
Authentic AI Search

Purpose:
Create fetch-ready search records from selected VRA sources.

Version:
1.0.0
=========================================================
"""

from typing import Any, Dict, List
from urllib.parse import urlparse


class QueryRetriever:
    """
    Converts selected source objects into normalized search records.

    Important:
    - Preserves all dynamic source intelligence metadata.
    - Builds candidate URLs for SourceFetcher.
    """

    def _normalize_url(
        self,
        url: str
    ) -> str:
        return (url or "").strip()

    def _domain_from_url(
        self,
        url: str
    ) -> str:
        parsed = urlparse(url)

        return (
            parsed.netloc
            .replace("www.", "")
            .lower()
            .strip()
        )

    def _candidate_urls(
        self,
        source: Dict[str, Any]
    ) -> List[str]:

        urls = []

        for key in [
            "base_url",
            "url",
            "source_url",
            "website",
        ]:
            url = self._normalize_url(
                source.get(key, "")
            )

            if url and url not in urls:
                urls.append(url)

        candidate_urls = source.get(
            "candidate_urls",
            []
        )

        if isinstance(candidate_urls, list):
            for url in candidate_urls:
                url = self._normalize_url(url)

                if url and url not in urls:
                    urls.append(url)

        return urls

    def build_search_queries(
        self,
        query_text: str,
        sources: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:

        search_records: List[Dict[str, Any]] = []

        for index, source in enumerate(
            sources,
            start=1
        ):
            candidate_urls = self._candidate_urls(source)

            if not candidate_urls:
                continue

            primary_url = candidate_urls[0]

            domain = (
                source.get("domain")
                or self._domain_from_url(primary_url)
            )

            search_records.append(
                {
                    "query": query_text,

                    "source_id": (
                        source.get("source_id")
                        or source.get("id")
                        or f"source_{index}_{domain}"
                    ),
                    "source_name": (
                        source.get("source_name")
                        or source.get("name")
                        or source.get("title")
                        or domain
                    ),
                    "source_url": primary_url,
                    "candidate_urls": candidate_urls,
                    "domain": domain,

                    "source_type": source.get("source_type"),
                    "source_category": source.get("source_category"),
                    "trust_tier": source.get("trust_tier"),

                    "authority_score": source.get("authority_score", 0),
                    "relevance_score": source.get("relevance_score", 0),
                    "coverage_score": source.get("coverage_score", 0),
                    "content_quality_score": source.get(
                        "content_quality_score",
                        0
                    ),
                    "freshness_signal_score": source.get(
                        "freshness_signal_score",
                        0
                    ),
                    "consensus_potential_score": source.get(
                        "consensus_potential_score",
                        0
                    ),
                    "discovery_score": source.get("discovery_score", 0),
                    "rank_score": source.get("rank_score", 0),
                    "source_quality_level": source.get(
                        "source_quality_level"
                    ),

                    "query_intent": source.get("query_intent"),
                    "is_official": source.get("is_official", False),
                    "is_trusted": source.get("is_trusted", False),
                    "authenticity_category": source.get(
                        "authenticity_category"
                    ),
                    "official_confidence_score": source.get(
                        "official_confidence_score",
                        0
                    ),
                    "source_risk_level": source.get(
                        "source_risk_level"
                    ),
                    "can_support_verified_answer": source.get(
                        "can_support_verified_answer",
                        False
                    ),

                    "dynamic": source.get("dynamic", False),
                    "registry_category": source.get("registry_category"),
                    "notes": source.get("notes"),
                    "search_query": source.get("search_query"),
                    "search_backend": source.get("search_backend"),
                }
            )

        return search_records