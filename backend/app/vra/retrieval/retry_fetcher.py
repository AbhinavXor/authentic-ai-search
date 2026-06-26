"""
=========================================================
MODULE: Source Fetcher

Project:
Authentic AI Search

Engine:
Verified Resource Algorithm (VRA)

Purpose:
Fetch source pages in parallel and extract clean evidence.

Version:
2.0.0
=========================================================
"""

from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Any, Dict, List, Optional

import requests
import urllib3
from bs4 import BeautifulSoup


urllib3.disable_warnings(
    urllib3.exceptions.InsecureRequestWarning
)


class SourceFetcher:
    """
    Parallel source fetcher for dynamic VRA search.
    """

    REQUEST_TIMEOUT = 8
    MAX_WORKERS = 10
    MIN_TEXT_LENGTH = 120
    MAX_TEXT_LENGTH = 15000
    MAX_CANDIDATE_URLS_PER_SOURCE = 3

    USER_AGENT = (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0 Safari/537.36 AuthenticAISearch/2.0"
    )

    BAD_CONTENT_MARKERS = {
        "access denied",
        "enable javascript",
        "captcha",
        "robot check",
        "forbidden",
        "page not found",
        "404 not found",
        "temporarily unavailable",
        "checking your browser",
        "cloudflare",
    }

    REMOVE_TAGS = [
        "script",
        "style",
        "noscript",
        "svg",
        "iframe",
        "form",
        "nav",
        "footer",
        "header",
        "aside",
        "button",
    ]

    CONTENT_TAGS = [
        "h1",
        "h2",
        "h3",
        "p",
        "li",
        "article",
        "main",
        "section",
    ]

    def clean_text(self, text: str) -> str:
        return " ".join((text or "").split())

    def extract_meta_content(
        self,
        soup: BeautifulSoup,
        name: str
    ) -> Optional[str]:

        meta_tag = soup.find(
            "meta",
            attrs={"name": name}
        )

        if not meta_tag:
            meta_tag = soup.find(
                "meta",
                attrs={"property": name}
            )

        if meta_tag and meta_tag.get("content"):
            return meta_tag.get("content").strip()

        return None

    def extract_title(
        self,
        soup: BeautifulSoup
    ) -> Optional[str]:

        for key in [
            "og:title",
            "twitter:title",
        ]:
            value = self.extract_meta_content(
                soup=soup,
                name=key
            )

            if value:
                return value

        if soup.title and soup.title.string:
            return soup.title.string.strip()

        h1 = soup.find("h1")

        if h1:
            return self.clean_text(
                h1.get_text(separator=" ")
            )

        return None

    def extract_description(
        self,
        soup: BeautifulSoup
    ) -> Optional[str]:

        for key in [
            "description",
            "og:description",
            "twitter:description",
        ]:
            value = self.extract_meta_content(
                soup=soup,
                name=key
            )

            if value:
                return value

        return None

    def extract_published_date(
        self,
        soup: BeautifulSoup,
        response_headers: Dict[str, Any]
    ) -> Optional[str]:

        date_keys = [
            "article:published_time",
            "article:modified_time",
            "date",
            "dc.date",
            "DC.date",
            "datePublished",
            "dateModified",
            "last-modified",
            "Last-Modified",
            "og:updated_time",
        ]

        for key in date_keys:
            value = self.extract_meta_content(
                soup=soup,
                name=key
            )

            if value:
                return value

        return response_headers.get("Last-Modified")

    def extract_page_text(
        self,
        soup: BeautifulSoup
    ) -> Optional[str]:

        for tag in soup(self.REMOVE_TAGS):
            tag.decompose()

        text_parts = []

        for tag in soup.find_all(self.CONTENT_TAGS):
            text = self.clean_text(
                tag.get_text(separator=" ")
            )

            if text and len(text) > 25:
                text_parts.append(text)

        if text_parts:
            page_text = self.clean_text(
                " ".join(text_parts)
            )
        else:
            page_text = self.clean_text(
                soup.get_text(separator=" ")
            )

        if not page_text:
            return None

        if len(page_text) < self.MIN_TEXT_LENGTH:
            return None

        return page_text[: self.MAX_TEXT_LENGTH]

    def _is_bad_content(
        self,
        page_text: Optional[str]
    ) -> bool:

        if not page_text:
            return True

        if len(page_text) < self.MIN_TEXT_LENGTH:
            return True

        lower_text = page_text.lower()

        return any(
            marker in lower_text
            for marker in self.BAD_CONTENT_MARKERS
        )

    def _unsupported_content_type(
        self,
        content_type: str
    ) -> bool:

        content_type = (content_type or "").lower()

        if not content_type:
            return False

        allowed_types = [
            "text/html",
            "application/xhtml",
            "application/xml",
        ]

        return not any(
            allowed in content_type
            for allowed in allowed_types
        )

    def fetch_url(
        self,
        url: str
    ) -> Dict[str, Any]:

        try:
            response = requests.get(
                url,
                timeout=self.REQUEST_TIMEOUT,
                verify=False,
                allow_redirects=True,
                headers={
                    "User-Agent": self.USER_AGENT,
                    "Accept": (
                        "text/html,application/xhtml+xml,"
                        "application/xml;q=0.9,*/*;q=0.8"
                    ),
                    "Accept-Language": "en-US,en;q=0.9",
                },
            )

            status_code = response.status_code
            final_url = response.url

            if status_code != 200:
                return {
                    "status": "failed",
                    "status_code": str(status_code),
                    "title": None,
                    "description": None,
                    "page_text": None,
                    "published_date": None,
                    "final_url": final_url,
                    "error": f"HTTP status code {status_code}",
                }

            content_type = response.headers.get(
                "Content-Type",
                ""
            )

            if self._unsupported_content_type(content_type):
                return {
                    "status": "failed",
                    "status_code": str(status_code),
                    "title": None,
                    "description": None,
                    "page_text": None,
                    "published_date": None,
                    "final_url": final_url,
                    "error": f"Unsupported content type {content_type}",
                }

            soup = BeautifulSoup(
                response.text,
                "html.parser"
            )

            title = self.extract_title(soup)
            description = self.extract_description(soup)
            page_text = self.extract_page_text(soup)

            if self._is_bad_content(page_text):
                return {
                    "status": "failed",
                    "status_code": str(status_code),
                    "title": title,
                    "description": description,
                    "page_text": page_text,
                    "published_date": None,
                    "final_url": final_url,
                    "error": "Empty or low-quality page content",
                }

            published_date = self.extract_published_date(
                soup=soup,
                response_headers=response.headers
            )

            return {
                "status": "success",
                "status_code": str(status_code),
                "title": title,
                "description": description,
                "page_text": page_text,
                "published_date": published_date,
                "final_url": final_url,
                "error": None,
            }

        except Exception as error:
            return {
                "status": "failed",
                "status_code": None,
                "title": None,
                "description": None,
                "page_text": None,
                "published_date": None,
                "final_url": url,
                "error": str(error),
            }

    def _candidate_urls(
        self,
        record: Dict[str, Any]
    ) -> List[str]:

        urls = []

        for url in record.get("candidate_urls", []):
            if url and url not in urls:
                urls.append(url)

        for key in [
            "source_url",
            "base_url",
            "url",
        ]:
            url = record.get(key)

            if url and url not in urls:
                urls.append(url)

        return urls[: self.MAX_CANDIDATE_URLS_PER_SOURCE]

    def _fetch_one_record(
        self,
        query_text: str,
        record: Dict[str, Any]
    ) -> Dict[str, Any]:

        candidate_urls = self._candidate_urls(record)

        fetched_data = None
        source_url = None

        for candidate_url in candidate_urls:
            fetched_data = self.fetch_url(candidate_url)

            source_url = (
                fetched_data.get("final_url")
                or candidate_url
            )

            if fetched_data.get("status") == "success":
                break

        if fetched_data is None:
            fetched_data = {
                "status": "failed",
                "status_code": None,
                "title": None,
                "description": None,
                "page_text": None,
                "published_date": None,
                "final_url": None,
                "error": "No candidate URL available",
            }

        return {
            "query": query_text,
            "source_id": record.get("source_id") or record.get("id"),
            "source_name": (
                record.get("source_name")
                or record.get("name")
                or fetched_data.get("title")
            ),
            "source_url": (
                source_url
                or record.get("source_url")
                or record.get("base_url")
                or record.get("url")
            ),
            "domain": record.get("domain"),
            "source_type": record.get("source_type"),
            "source_category": record.get("source_category"),
            "trust_tier": record.get("trust_tier"),
            "authority_score": record.get("authority_score", 0),
            "relevance_score": record.get("relevance_score", 0),
            "coverage_score": record.get("coverage_score", 0),
            "content_quality_score": record.get(
                "content_quality_score",
                0
            ),
            "freshness_signal_score": record.get(
                "freshness_signal_score",
                0
            ),
            "consensus_potential_score": record.get(
                "consensus_potential_score",
                0
            ),
            "discovery_score": record.get("discovery_score", 0),
            "rank_score": record.get("rank_score", 0),
            "source_quality_level": record.get("source_quality_level"),
            "query_intent": record.get("query_intent"),
            "is_official": record.get("is_official", False),
            "is_trusted": record.get("is_trusted", False),
            "authenticity_category": record.get(
                "authenticity_category"
            ),
            "official_confidence_score": record.get(
                "official_confidence_score",
                0
            ),
            "source_risk_level": record.get(
                "source_risk_level"
            ),
            "can_support_verified_answer": record.get(
                "can_support_verified_answer",
                False
            ),
            "retrieval_status": fetched_data.get("status"),
            "status_code": fetched_data.get("status_code"),
            "page_title": fetched_data.get("title"),
            "page_description": fetched_data.get("description"),
            "page_text": fetched_data.get("page_text"),
            "published_date": fetched_data.get("published_date"),
            "error": fetched_data.get("error"),
        }

    def fetch_from_search_records(
        self,
        query_text: str,
        search_records: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:

        if not search_records:
            return []

        evidence_records: List[Dict[str, Any]] = []

        max_workers = min(
            self.MAX_WORKERS,
            max(1, len(search_records))
        )

        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            future_to_record = {
                executor.submit(
                    self._fetch_one_record,
                    query_text,
                    record
                ): record
                for record in search_records
            }

            for future in as_completed(future_to_record):
                try:
                    evidence_records.append(
                        future.result()
                    )

                except Exception as error:
                    record = future_to_record[future]

                    evidence_records.append(
                        {
                            "query": query_text,
                            "source_id": record.get("source_id") or record.get("id"),
                            "source_name": record.get("source_name") or record.get("name"),
                            "source_url": record.get("source_url") or record.get("base_url"),
                            "domain": record.get("domain"),
                            "source_type": record.get("source_type"),
                            "authority_score": record.get("authority_score", 0),
                            "retrieval_status": "failed",
                            "status_code": None,
                            "page_title": None,
                            "page_description": None,
                            "page_text": None,
                            "published_date": None,
                            "error": str(error),
                        }
                    )

        evidence_records.sort(
            key=lambda record: (
                float(record.get("rank_score", 0) or 0),
                float(record.get("authority_score", 0) or 0),
            ),
            reverse=True
        )

        return evidence_records