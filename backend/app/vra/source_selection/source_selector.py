"""
=========================================================
MODULE: Source Selector

Project:
Authentic AI Search

Engine:
Verified Resource Algorithm (VRA)

Purpose:
Select the best trusted sources for a user query.

Author:
Abhinav

Version:
1.2.0
=========================================================
"""

import re
from typing import Any, Dict, List


class SourceSelector:
    """
    Selects trusted sources using:
    - hard entity matching
    - query relevance
    - authority score
    - category match

    Important:
    Sources with zero query relevance are rejected for query-based searches.
    This prevents unrelated high-authority sources from polluting answers.
    """

    def __init__(self) -> None:
        self.stopwords = {
            "what",
            "is",
            "are",
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
            "who",
            "when",
            "where",
            "why",
            "how",
            "explain",
            "tell",
            "me",
            "about"
        }

    def _tokenize(
        self,
        text: str
    ) -> List[str]:
        """
        Convert text into searchable tokens.
        """

        if not text:
            return []

        words = re.findall(
            r"[a-zA-Z0-9]+",
            text.lower()
        )

        return [
            word
            for word in words
            if word not in self.stopwords
        ]

    def _build_source_text(
        self,
        source: Dict[str, Any]
    ) -> str:
        """
        Build searchable text from source metadata.
        """

        fields = [
            source.get("name", ""),
            source.get("title", ""),
            source.get("domain", ""),
            source.get("url", ""),
            source.get("base_url", ""),
            source.get("description", ""),
            source.get("source_type", ""),
            source.get("registry_category", "")
        ]

        keywords = source.get("keywords")

        if isinstance(keywords, list):
            fields.extend(keywords)

        elif isinstance(keywords, str):
            fields.append(keywords)

        return " ".join(
            str(field)
            for field in fields
            if field
        )

    def _hard_match_sources(
        self,
        query_text: str,
        sources: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """
        Return exact trusted sources for known official entities.
        """

        query_lower = query_text.lower()

        hard_match_rules = {
            "mospi": ["mospi.gov.in"],
            "ministry of statistics": ["mospi.gov.in"],
            "ministry of statistics and programme implementation": [
                "mospi.gov.in"
            ],
            "ministry of statistics and program implementation": [
                "mospi.gov.in"
            ],
            "rbi": ["rbi.org.in"],
            "reserve bank": ["rbi.org.in"],
            "reserve bank of india": ["rbi.org.in"],
            "census": ["censusindia.gov.in"],
            "census of india": ["censusindia.gov.in"],
            "who": ["who.int"],
            "world health organization": ["who.int"],
            "imf": ["imf.org"],
            "international monetary fund": ["imf.org"],
            "world bank": ["worldbank.org"],
        }

        matched_domains: List[str] = []

        for keyword, domains in hard_match_rules.items():
            if keyword in query_lower:
                matched_domains.extend(domains)

        if not matched_domains:
            return []

        matched_domain_set = set(matched_domains)

        matched_sources: List[Dict[str, Any]] = []

        for source in sources:
            domain = str(
                source.get("domain", "")
            ).lower()

            if domain in matched_domain_set:
                source_copy = dict(source)
                source_copy["selection_score"] = 100.0
                source_copy["query_relevance_score"] = 100.0
                source_copy["selection_reason"] = "hard_entity_match"
                matched_sources.append(source_copy)

        matched_sources = sorted(
            matched_sources,
            key=lambda source: float(
                source.get("authority_score", 0)
            ),
            reverse=True
        )

        return matched_sources

    def _query_relevance_score(
        self,
        query_text: str,
        source: Dict[str, Any]
    ) -> float:
        """
        Score source relevance against query.
        """

        query_tokens = self._tokenize(
            query_text
        )

        if not query_tokens:
            return 0.0

        source_text = self._build_source_text(
            source
        ).lower()

        score = 0.0

        for token in query_tokens:
            if token in source_text:
                score += 20.0

        compact_query = " ".join(query_tokens)

        if compact_query and compact_query in source_text:
            score += 40.0

        name = str(
            source.get("name", "")
            or source.get("title", "")
        ).lower()

        domain = str(
            source.get("domain", "")
        ).lower()

        for token in query_tokens:
            if token in name:
                score += 20.0

            if token in domain:
                score += 15.0

        return min(score, 100.0)

    def _category_score(
        self,
        source: Dict[str, Any],
        category: str
    ) -> float:
        """
        Score category match.
        """

        if not category:
            return 0.0

        if source.get("registry_category") == category:
            return 30.0

        return 0.0

    def select_sources(
        self,
        sources: List[Dict[str, Any]],
        category: str,
        limit: int = 5,
        query_text: str | None = None
    ) -> List[Dict[str, Any]]:
        """
        Select best sources for a query.
        """

        if query_text:
            hard_matches = self._hard_match_sources(
                query_text=query_text,
                sources=sources
            )

            if hard_matches:
                return hard_matches[:limit]

        scored_sources: List[Dict[str, Any]] = []

        for source in sources:
            authority_score = float(
                source.get("authority_score", 0)
            )

            relevance_score = 0.0

            if query_text:
                relevance_score = self._query_relevance_score(
                    query_text=query_text,
                    source=source
                )

            if query_text and relevance_score <= 0:
                continue

            category_score = self._category_score(
                source=source,
                category=category
            )

            final_score = (
                relevance_score * 0.75
                + authority_score * 0.20
                + category_score * 0.05
            )

            source_copy = dict(source)
            source_copy["selection_score"] = round(final_score, 2)
            source_copy["query_relevance_score"] = round(
                relevance_score,
                2
            )
            source_copy["selection_reason"] = "query_relevance_match"

            scored_sources.append(source_copy)

        ranked_sources = sorted(
            scored_sources,
            key=lambda source: source.get(
                "selection_score",
                0
            ),
            reverse=True
        )

        return ranked_sources[:limit]