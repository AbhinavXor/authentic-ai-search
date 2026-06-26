"""
=========================================================
MODULE: Source Fetcher

Project:
Authentic AI Search

Engine:
Verified Resource Algorithm (VRA)

Purpose:
Fetch source pages and extract clean evidence.

Version:
1.0.0
=========================================================
"""

import logging
import random
import re
import time
from typing import Any, Dict, List, Optional

import requests
import urllib3
from bs4 import BeautifulSoup
from requests.adapters import HTTPAdapter

from backend.app.vra.retrieval.html_content_extractor import HTMLContentExtractor

try:
    from urllib3.util.retry import Retry
except ImportError:  # pragma: no cover
    Retry = None


urllib3.disable_warnings(
    urllib3.exceptions.InsecureRequestWarning
)

logger = logging.getLogger(__name__)


class SourceFetcher:
    """
    Fetches source pages and extracts useful metadata/text.
    """

    REQUEST_TIMEOUT = 6
    MIN_TEXT_LENGTH = 80
    MAX_TEXT_LENGTH = 12000

    MIN_PARTIAL_TEXT_LENGTH = 80

    MAX_RETRIES = 3
    BACKOFF_SCHEDULE = [1, 2, 4]
    RETRY_STATUS_CODES = {429, 500, 502, 503, 504}

    USER_AGENTS = [
        # Chrome - Windows
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0.0.0 Safari/537.36",
        # Chrome - Mac
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0.0.0 Safari/537.36",
        # Firefox - Windows
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:125.0) "
        "Gecko/20100101 Firefox/125.0",
        # Firefox - Mac
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:125.0) "
        "Gecko/20100101 Firefox/125.0",
        # Safari - Mac
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/605.1.15 (KHTML, like Gecko) "
        "Version/17.4 Safari/605.1.15",
        # Chrome - Linux
        "Mozilla/5.0 (X11; Linux x86_64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0.0.0 Safari/537.36",
    ]

    def __init__(self) -> None:
        self.html_extractor = HTMLContentExtractor()
        self.session = self._build_session()

    def _build_session(self) -> requests.Session:
        session = requests.Session()

        if Retry is not None:
            retry = Retry(
                total=self.MAX_RETRIES,
                backoff_factor=1,
                status_forcelist=list(self.RETRY_STATUS_CODES),
                allowed_methods=frozenset(["GET", "HEAD"]),
                raise_on_status=False,
                respect_retry_after_header=True,
            )
            adapter = HTTPAdapter(max_retries=retry)
            session.mount("http://", adapter)
            session.mount("https://", adapter)

        return session

    def _random_user_agent(self) -> str:
        return random.choice(self.USER_AGENTS)

    def _build_headers(self) -> Dict[str, str]:
        return {
            "User-Agent": self._random_user_agent(),
            "Accept": (
                "text/html,application/xhtml+xml,"
                "application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8"
            ),
            "Accept-Language": "en-US,en;q=0.9",
            "Accept-Encoding": "gzip, deflate, br",
            "Cache-Control": "no-cache",
            "Upgrade-Insecure-Requests": "1",
            "Referer": "https://www.google.com/",
        }

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

    def extract_published_date(
        self,
        soup: BeautifulSoup,
        response_headers: Dict[str, Any]
    ) -> Optional[str]:

        date_candidates = [
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

        for key in date_candidates:
            meta_value = self.extract_meta_content(
                soup=soup,
                name=key
            )

            if meta_value:
                return meta_value

        header_date = response_headers.get(
            "Last-Modified"
        )

        if header_date:
            return header_date

        return None

    def _fallback_extract_text(
        self,
        html: str,
    ) -> Dict[str, Optional[str]]:
        """
        Fallback extraction used when HTMLContentExtractor fails or
        returns too little text. Strips non-content tags, collects
        text from article/main/[role="main"]/body (in that priority
        order), and-if that text is too thin-falls back further to
        paragraph- and list-level tags. Normalizes whitespace and
        truncates to MAX_TEXT_LENGTH.
        """

        try:
            soup = BeautifulSoup(html, "lxml")
        except Exception:
            soup = BeautifulSoup(html, "html.parser")

        for tag_name in (
            "script",
            "style",
            "noscript",
            "svg",
            "canvas",
            "iframe",
            "form",
            "button",
            "nav",
            "footer",
            "header",
            "aside",
        ):
            for tag in soup.find_all(tag_name):
                tag.decompose()

        title = None
        if soup.title and soup.title.string:
            title = soup.title.string.strip()

        description = self.extract_meta_content(
            soup=soup,
            name="description",
        ) or self.extract_meta_content(
            soup=soup,
            name="og:description",
        )

        content_node = (
            soup.find("article")
            or soup.find("main")
            or soup.find(attrs={"role": "main"})
            or soup.find("body")
        )

        raw_text = content_node.get_text(separator=" ") if content_node else ""
        normalized_text = re.sub(r"\s+", " ", raw_text).strip()

        if len(normalized_text) < self.MIN_TEXT_LENGTH:
            block_tags = soup.find_all(["p", "li", "h1", "h2", "h3"])
            block_text = " ".join(
                tag.get_text(separator=" ") for tag in block_tags
            )
            block_text = re.sub(r"\s+", " ", block_text).strip()

            if len(block_text) > len(normalized_text):
                normalized_text = block_text

        if len(normalized_text) > self.MAX_TEXT_LENGTH:
            normalized_text = normalized_text[: self.MAX_TEXT_LENGTH]

        return {
            "title": title,
            "description": description,
            "page_text": normalized_text,
        }

    def _is_bad_content(
        self,
        page_text: Optional[str]
    ) -> bool:

        if not page_text:
            return True

        stripped_text = page_text.strip()

        if len(stripped_text) < 60:
            return True

        lower_text = page_text.lower()

        bad_markers = [
            "captcha",
            "cloudflare challenge",
            "checking your browser",
            "access denied",
            "enable javascript",
            "robot check",
            "please enable cookies",
            "ddos protection",
            "browser verification",
            "security check to access",
        ]

        return any(
            marker in lower_text
            for marker in bad_markers
        )

    def _log_failed_fetch(
        self,
        url: str,
        final_url: Optional[str],
        status_code: Optional[Any],
        content_type: Optional[str],
        reason: str,
    ) -> None:
        logger.warning(
            "SourceFetcher failed fetch | url=%s | final_url=%s | "
            "status=%s | content_type=%s | reason=%s",
            url,
            final_url,
            status_code,
            content_type,
            reason,
        )

    def _request_with_retries(
        self,
        url: str,
    ) -> requests.Response:
        last_error: Optional[Exception] = None

        for attempt in range(self.MAX_RETRIES + 1):
            try:
                response = self.session.get(
                    url,
                    timeout=self.REQUEST_TIMEOUT,
                    verify=False,
                    allow_redirects=True,
                    headers=self._build_headers(),
                )

                if (
                    response.status_code in self.RETRY_STATUS_CODES
                    and attempt < self.MAX_RETRIES
                ):
                    sleep_seconds = self.BACKOFF_SCHEDULE[
                        min(attempt, len(self.BACKOFF_SCHEDULE) - 1)
                    ]
                    time.sleep(sleep_seconds)
                    continue

                return response

            except requests.exceptions.Timeout as error:
                last_error = error
                if attempt < self.MAX_RETRIES:
                    sleep_seconds = self.BACKOFF_SCHEDULE[
                        min(attempt, len(self.BACKOFF_SCHEDULE) - 1)
                    ]
                    time.sleep(sleep_seconds)
                    continue
                raise
            except requests.exceptions.RequestException as error:
                last_error = error
                if attempt < self.MAX_RETRIES:
                    sleep_seconds = self.BACKOFF_SCHEDULE[
                        min(attempt, len(self.BACKOFF_SCHEDULE) - 1)
                    ]
                    time.sleep(sleep_seconds)
                    continue
                raise

        if last_error:
            raise last_error

        raise requests.exceptions.RequestException(
            f"Failed to fetch {url} after {self.MAX_RETRIES} retries"
        )

    def fetch_url(
        self,
        url: str
    ) -> Dict[str, Optional[str]]:

        try:
            response = self._request_with_retries(url)

            status_code = response.status_code
            content_type = response.headers.get(
                "Content-Type",
                ""
            ).lower()

            if status_code != 200:
                self._log_failed_fetch(
                    url=url,
                    final_url=response.url,
                    status_code=status_code,
                    content_type=content_type,
                    reason=f"HTTP status code {status_code}",
                )
                return {
                    "status": "failed",
                    "status_code": str(status_code),
                    "title": None,
                    "description": None,
                    "page_text": None,
                    "published_date": None,
                    "final_url": response.url,
                    "error": f"HTTP status code {status_code}",
                }

            if (
                "text/html" not in content_type
                and "application/xhtml" not in content_type
                and content_type
            ):
                self._log_failed_fetch(
                    url=url,
                    final_url=response.url,
                    status_code=status_code,
                    content_type=content_type,
                    reason=f"Unsupported content type {content_type}",
                )
                return {
                    "status": "failed",
                    "status_code": str(status_code),
                    "title": None,
                    "description": None,
                    "page_text": None,
                    "published_date": None,
                    "final_url": response.url,
                    "error": f"Unsupported content type {content_type}",
                }

            # Ensure we decode the body with the best-guess encoding
            # rather than trusting a missing/incorrect header charset.
            response.encoding = response.apparent_encoding or response.encoding

            extracted = self.html_extractor.extract(
                html=response.text,
                source_url=response.url,
            )

            title = None
            description = None
            page_text = None

            if extracted.get("status") == "success":
                title = extracted.get("page_title")
                description = extracted.get("page_description")
                page_text = extracted.get("page_text")

            if not page_text or len(page_text.strip()) < self.MIN_PARTIAL_TEXT_LENGTH:
                fallback = self._fallback_extract_text(html=response.text)

                title = title or fallback.get("title")
                description = description or fallback.get("description")

                fallback_text = fallback.get("page_text") or ""

                if not page_text or len(fallback_text) > len(page_text or ""):
                    page_text = fallback_text

            soup = BeautifulSoup(response.text, "lxml")

            page_text_length = len(page_text.strip()) if page_text else 0

            if (
                page_text_length < self.MIN_PARTIAL_TEXT_LENGTH
                or self._is_bad_content(page_text)
            ):
                self._log_failed_fetch(
                    url=url,
                    final_url=response.url,
                    status_code=status_code,
                    content_type=content_type,
                    reason="Empty or low-quality page content",
                )
                return {
                    "status": "failed",
                    "status_code": str(status_code),
                    "title": title,
                    "description": description,
                    "page_text": page_text,
                    "published_date": None,
                    "final_url": response.url,
                    "error": "Empty or low-quality page content",
                }

            published_date = self.extract_published_date(
                soup=soup,
                response_headers=response.headers,
            )

            return {
                "status": "success",
                "status_code": str(status_code),
                "title": title,
                "description": description,
                "page_text": page_text,
                "published_date": published_date,
                "final_url": response.url,
                "error": None,
            }

        except Exception as error:
            self._log_failed_fetch(
                url=url,
                final_url=None,
                status_code=None,
                content_type=None,
                reason=str(error),
            )
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

    def fetch_from_search_records(
        self,
        query_text: str,
        search_records: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:

        evidence_records: List[Dict[str, Any]] = []

        for record in search_records:
            candidate_urls = record.get(
                "candidate_urls",
                []
            )

            fetched_data = None
            source_url = None

            for candidate_url in candidate_urls:
                fetched_data = self.fetch_url(
                    candidate_url
                )

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

            evidence_records.append(
                {
                    "query": query_text,
                    "source_id": record.get("source_id"),
                    "source_name": record.get("source_name"),
                    "source_url": source_url or record.get("source_url"),
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
                    "discovery_score": record.get("discovery_score", 0),
                    "rank_score": record.get("rank_score", 0),
                    "is_official": record.get("is_official", False),
                    "is_trusted": record.get("is_trusted", False),
                    "authenticity_category": record.get(
                        "authenticity_category"
                    ),
                    "official_confidence_score": record.get(
                        "official_confidence_score",
                        0
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
            )

        return evidence_records