"""
=========================================================
MODULE: Free Search Provider

Project:
Authentic AI Search

Purpose:
Deep dynamic internet search for VRA source discovery.

Version:
2.0.0
=========================================================
"""

import time
from typing import Any, Dict, List, Optional
from urllib.parse import urlparse

try:
    from ddgs import DDGS
except ImportError:
    from duckduckgo_search import DDGS


class FreeSearchProvider:
    """
    Performs broad dynamic internet search.

    Key behavior:
    - No fixed entity dependency
    - Multiple query variants
    - Multiple DDGS backends
    - URL dedupe
    - Domain diversity
    - Stops by time, no-new-results, or safety max_results
    """

    SEARCH_BACKENDS = (
        "lite",
        "html",
    )

    SEARCH_SUFFIXES = (
        "",
        "official source",
        "official website",
        "trusted source",
        "definition",
        "explanation",
        "government source",
        "institutional source",
        "site:.gov",
        "site:.org",
        "site:.edu",
        "site:.int",
    )

    def _domain_from_url(
        self,
        url: str
    ) -> str:
        parsed_url = urlparse(url)

        return (
            parsed_url.netloc
            .replace("www.", "")
            .lower()
            .strip()
        )

    def _clean_query(
        self,
        query_text: str
    ) -> str:
        return " ".join(
            query_text.strip().split()
        )

    def _build_search_queries(
        self,
        query_text: str
    ) -> List[str]:
        """
        Build broad query variants without hardcoding entities.
        """

        query = self._clean_query(query_text)

        search_queries: List[str] = []
        seen_queries = set()

        for suffix in self.SEARCH_SUFFIXES:
            if suffix:
                search_query = f"{query} {suffix}"
            else:
                search_query = query

            normalized = search_query.lower().strip()

            if normalized in seen_queries:
                continue

            seen_queries.add(normalized)
            search_queries.append(search_query)

        return search_queries

    def _normalize_result(
        self,
        item: Dict[str, Any],
        search_query: str,
        backend: str
    ) -> Optional[Dict[str, Any]]:
        """
        Convert DDGS result into normalized VRA search result.
        """

        url = (
            item.get("href")
            or item.get("url")
            or item.get("link")
        )

        if not url:
            return None

        if not (
            url.startswith("http://")
            or url.startswith("https://")
        ):
            return None

        domain = self._domain_from_url(url)

        if not domain:
            return None

        title = item.get("title", "") or ""

        snippet = (
            item.get("body", "")
            or item.get("snippet", "")
            or item.get("description", "")
            or ""
        )

        return {
            "title": title.strip(),
            "url": url.strip(),
            "domain": domain,
            "snippet": snippet.strip(),
            "source": "duckduckgo",
            "search_query": search_query,
            "search_backend": backend,
        }

    def search(
        self,
        query_text: str,
        max_results: int = 200,
        max_runtime_seconds: int = 25,
        max_empty_rounds: int = 6,
        max_results_per_domain: int = 4
    ) -> List[Dict[str, Any]]:
        """
        Perform deep dynamic search.

        max_results is only a safety cap. The search keeps collecting
        until time limit, no-new-results limit, or available results end.
        """

        if not query_text or not query_text.strip():
            return []

        results: List[Dict[str, Any]] = []

        seen_urls = set()
        domain_counts: Dict[str, int] = {}

        started_at = time.time()
        empty_rounds = 0

        search_queries = self._build_search_queries(
            query_text
        )

        for search_query in search_queries:

            if time.time() - started_at >= max_runtime_seconds:
                break

            query_added_count = 0

            for backend in self.SEARCH_BACKENDS:

                if time.time() - started_at >= max_runtime_seconds:
                    break

                try:
                    with DDGS() as ddgs:
                        search_items = ddgs.text(
                            search_query,
                            max_results=max_results,
                            backend=backend
                        )

                        backend_added_count = 0

                        for item in search_items:

                            if time.time() - started_at >= max_runtime_seconds:
                                break

                            normalized_result = self._normalize_result(
                                item=item,
                                search_query=search_query,
                                backend=backend
                            )

                            if not normalized_result:
                                continue

                            url = normalized_result["url"]
                            domain = normalized_result["domain"]

                            if url in seen_urls:
                                continue

                            current_domain_count = domain_counts.get(
                                domain,
                                0
                            )

                            if current_domain_count >= max_results_per_domain:
                                continue

                            seen_urls.add(url)

                            domain_counts[domain] = (
                                current_domain_count + 1
                            )

                            results.append(
                                normalized_result
                            )

                            query_added_count += 1
                            backend_added_count += 1

                            if len(results) >= max_results:
                                return results

                        if backend_added_count == 0:
                            empty_rounds += 1
                        else:
                            empty_rounds = 0

                        if empty_rounds >= max_empty_rounds:
                            return results

                except Exception as error:
                    print(
                        f"DDGS backend failed [{backend}] "
                        f"query=[{search_query}]: {error}"
                    )

                    empty_rounds += 1

                    if empty_rounds >= max_empty_rounds:
                        return results

            if query_added_count == 0:
                empty_rounds += 1
            else:
                empty_rounds = 0

            if empty_rounds >= max_empty_rounds:
                break

        return results