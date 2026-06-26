"""
=========================================================
MODULE: Source Discovery

Project:
Authentic AI Search

Engine:
Verified Resource Algorithm (VRA)

Purpose:
Discover query-relevant source URLs.

Author:
Abhinav

Version:
0.1.0
=========================================================
"""

from typing import Any, Dict, List


class SourceDiscovery:
    """
    MVP source discovery.

    Current:
    - Uses simple query/domain rules
    - Returns source URL to fetch

    Future:
    - Search engine integration
    - Sitemap parsing
    - API-based discovery
    """

    def discover_urls(
        self,
        query_text: str,
        sources: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        updated_sources = []

        query_lower = query_text.lower()

        for source in sources:
            source_copy = dict(source)
            base_url = source.get("base_url", "")

            discovered_url = base_url

            if "population" in query_lower:
                if source.get("domain") == "mospi.gov.in":
                    discovered_url = "https://www.mospi.gov.in"

                elif source.get("domain") == "censusindia.gov.in":
                    discovered_url = "https://censusindia.gov.in"

            source_copy["discovered_url"] = discovered_url
            updated_sources.append(source_copy)

        return updated_sources