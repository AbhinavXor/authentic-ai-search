"""
=========================================================
MODULE: HTML Content Extractor

Project:
Authentic AI Search

Engine:
VRA Search Engine

Purpose:
Extract clean readable content, title, description,
headings, and metadata from raw HTML.

Version:
2.0.0
=========================================================
"""

from typing import Any, Dict, List, Optional
import re

from bs4 import BeautifulSoup


class HTMLContentExtractor:
    """
    Extracts useful readable content from raw HTML.

    Goal:
    - Remove navigation, footer, sidebar, share buttons, ads.
    - Prefer article/main/body content.
    - Prefer paragraph content over menus/lists.
    - Return clean page_text for ClaimExtractor.
    """

    def __init__(
        self,
        max_text_chars: int = 12000
    ) -> None:
        self.max_text_chars = max_text_chars

    NOISE_TAGS = [
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
        "menu",
        "dialog",
        "video",
        "audio",
    ]

    NOISE_SELECTORS = [
        ".sidebar",
        ".footer",
        ".header",
        ".breadcrumb",
        ".breadcrumbs",
        ".toc",
        ".table-of-contents",
        ".related",
        ".related-content",
        ".recommended",
        ".recommend",
        ".newsletter",
        ".social",
        ".share",
        ".sharing",
        ".advertisement",
        ".ads",
        ".ad",
        ".promo",
        ".cookie",
        ".cookies",
        ".modal",
        ".popup",
        ".nav",
        ".navbar",
        ".menu",
        ".pagination",
        ".comments",
        ".comment",
        ".author-card",
        ".byline",
        ".mw-editsection",
        ".mw-jump-link",
        ".vector-toc",
        ".navbox",
        ".reflist",
        "sup.reference",
        ".mw-cite-backlink",
    ]

    BAD_TEXT_MARKERS = {
        "share this page",
        "share on facebook",
        "share on twitter",
        "share on linkedin",
        "share on email",
        "subscribe",
        "newsletter",
        "cookie policy",
        "privacy policy",
        "terms of use",
        "all rights reserved",
        "skip to content",
        "skip to main content",
        "table of contents",
        "related pages",
        "view more",
        "read more",
        "featured speaker",
        "featured on:",
        "print updated",
        "download csv",
        "download xml",
        "download excel",
        "download pdf",
        "video q&a",
        "details preview",
        "openai openai",
        "summer update",
        "gpt-5 is here",
        "product 7 min read",
        "research 5 min read",
        "security 8 min read",
    }

    STRONG_DESCRIPTION_NOISE_MARKERS = [
        "cookie policy",
        "privacy policy",
        "terms of use",
        "subscribe",
        "newsletter",
    ]

    # Generic substrings used by `_remove_noise` to catch noise containers
    # via class/id/role (e.g. "site-nav", "ad-banner"). Some real words
    # contain these substrings without being noise (e.g. "navy" contains
    # "nav", "commentary" contains "comment"). These whole-token words are
    # excluded from the sweep so legitimate content roots/sections are not
    # accidentally decomposed.
    NOISE_MARKER_SAFE_WORDS = {
        "navy",
        "naval",
        "navigator",
        "commentary",
        "commentator",
        "shareholder",
        "shareholders",
        "shared",
        "sharepoint",
        "headers",
        "adventure",
        "adverse",
        "advertised",
    }

    ENCODING_ARTIFACT_MAP = {
     "â€™": "'",
     "â€˜": "'",
     "â€œ": '"',
     "â€": '"',
     "â€�": '"',
     "â€“": "-",
     "â€”": "-",
     "â€¦": "...",
     "Â ": " ",
     "Â": "",
    }

    # Legitimate Unicode punctuation (not mojibake) normalized to plain
    # ASCII equivalents for consistent downstream text processing.
    UNICODE_PUNCTUATION_MAP = {
        "\u2018": "'",
        "\u2019": "'",
        "\u201a": "'",
        "\u201b": "'",
        "\u201c": '"',
        "\u201d": '"',
        "\u201e": '"',
        "\u201f": '"',
        "\u2013": "-",
        "\u2014": "-",
        "\u2015": "-",
        "\u2026": "...",
        "\u00a0": " ",
    }

    _UNICODE_PUNCTUATION_TABLE = str.maketrans(UNICODE_PUNCTUATION_MAP)

    def _normalize_encoding_artifacts(
        self,
        text: str
    ) -> str:
        if not text:
            return text

        for bad_sequence, replacement in self.ENCODING_ARTIFACT_MAP.items():
            if bad_sequence in text:
                text = text.replace(bad_sequence, replacement)

        return text

    def _clean_text(
        self,
        text: Optional[str]
    ) -> str:
        if not text:
            return ""

        text = str(text)
        text = self._normalize_encoding_artifacts(text)
        text = text.translate(self._UNICODE_PUNCTUATION_TABLE)
        text = re.sub(r"\s+", " ", text)
        text = text.replace(" ,", ",")
        text = text.replace(" .", ".")
        text = text.replace(" :", ":")
        text = text.replace("( ", "(")
        text = text.replace(" )", ")")

        return text.strip()

    def _is_bad_text(
        self,
        text: str
    ) -> bool:
        """
        Mild filter for generic metadata/headings. Only rejects
        truly empty or near-empty text so short but valid items
        like "Elon Musk" or "GDP" are not dropped.
        """
        text = self._clean_text(text)

        if not text:
            return True

        if len(text) < 3:
            return True

        return False

    def _is_bad_content_chunk(
        self,
        text: str
    ) -> bool:
        """
        Stricter filter used for body paragraph/list/blockquote
        chunks, where navigation, share, cookie, and other boiler-
        plate noise should be excluded.
        """
        text = self._clean_text(text)
        text_lower = text.lower()

        if not text:
            return True

        if len(text) < 30:
            return True

        if any(
            marker in text_lower
            for marker in self.BAD_TEXT_MARKERS
        ):
            return True

        if text_lower.count("|") >= 2:
            return True

        if text_lower.count(" share ") >= 3:
            return True

        if text_lower.count(" read ") >= 3:
            return True

        if text_lower.count(" view ") >= 3:
            return True

        return False

    def _matches_noise_marker(
        self,
        combined: str,
        markers: List[str]
    ) -> bool:
        """
        Checks whether any noise marker appears inside a class/id/role
        string, tokenized on non-alphanumeric boundaries. Whole tokens
        present in NOISE_MARKER_SAFE_WORDS are skipped so that words like
        "navy" or "commentary" don't trigger on the "nav"/"comment"
        markers. Compound tokens such as "submenu" or "site-nav" still
        match, since the substring check runs per-token.
        """
        tokens = re.findall(r"[a-z0-9]+", combined.lower())

        for token in tokens:
            if token in self.NOISE_MARKER_SAFE_WORDS:
                continue

            for marker in markers:
                if marker in token:
                    return True

        return False

    def _remove_noise(
        self,
        soup: BeautifulSoup
    ) -> None:
        for tag_name in self.NOISE_TAGS:
            for tag in soup.find_all(tag_name):
                tag.decompose()

        for selector in self.NOISE_SELECTORS:
            for tag in soup.select(selector):
                tag.decompose()

        sweep_markers = [
            "sidebar",
            "breadcrumb",
            "related",
            "recommend",
            "newsletter",
            "social",
            "share",
            "advert",
            "cookie",
            "popup",
            "modal",
            "menu",
            "nav",
            "footer",
            "header",
            "comment",
        ]

        for tag in soup.find_all(True):
            class_text = " ".join(tag.get("class", [])).lower()
            id_text = str(tag.get("id", "") or "").lower()
            role_text = str(tag.get("role", "") or "").lower()

            combined = f"{class_text} {id_text} {role_text}"

            if self._matches_noise_marker(combined, sweep_markers):
                tag.decompose()

    def _extract_title(
        self,
        soup: BeautifulSoup
    ) -> str:
        for attrs in [
            {"property": "og:title"},
            {"name": "twitter:title"},
            {"itemprop": "headline"},
            {"itemprop": "name"},
        ]:
            tag = soup.find("meta", attrs=attrs)
            if tag and tag.get("content"):
                return self._clean_text(tag.get("content"))

        if soup.title and soup.title.string:
            return self._clean_text(soup.title.string)

        h1 = soup.find("h1")
        if h1:
            return self._clean_text(
                h1.get_text(" ", strip=True)
            )

        return ""

    def _extract_description(
        self,
        soup: BeautifulSoup
    ) -> str:
        for attrs in [
            {"name": "description"},
            {"property": "og:description"},
            {"name": "twitter:description"},
            {"itemprop": "description"},
        ]:
            tag = soup.find("meta", attrs=attrs)

            if not tag or not tag.get("content"):
                continue

            description = self._clean_text(
                tag.get("content")
            )

            if not description:
                continue

            description_lower = description.lower()

            if any(
                marker in description_lower
                for marker in self.STRONG_DESCRIPTION_NOISE_MARKERS
            ):
                continue

            return description

        return ""

    def _extract_metadata(
        self,
        soup: BeautifulSoup
    ) -> Dict[str, Any]:
        metadata: Dict[str, Any] = {}

        for tag in soup.find_all("meta"):
            key = (
                tag.get("name")
                or tag.get("property")
                or tag.get("itemprop")
            )

            value = tag.get("content")

            if not key or not value:
                continue

            clean_key = self._clean_text(key)
            clean_value = self._clean_text(value)

            if clean_key and clean_value:
                metadata[clean_key] = clean_value

        return metadata

    def _extract_headings(
        self,
        soup: BeautifulSoup
    ) -> List[str]:
        headings: List[str] = []

        for tag in soup.find_all(["h1", "h2", "h3"]):
            text = self._clean_text(
                tag.get_text(" ", strip=True)
            )

            if self._is_bad_text(text):
                continue

            headings.append(text)

        headings = self._dedupe_chunks(headings)

        return headings[:30]

    def _best_content_root(
        self,
        soup: BeautifulSoup
    ):
        candidates = [
            soup.find("article"),
            soup.find("main"),
            soup.find(attrs={"role": "main"}),
            soup.select_one(".mw-parser-output"),
            soup.find(id="mw-content-text"),
            soup.find(id="content"),
            soup.select_one(".story-body"),
            soup.select_one(".post-content"),
            soup.select_one(".entry-content"),
            soup.select_one(".article-content"),
            soup.select_one(".body-content"),
            soup.select_one(".content"),
            soup.find("body"),
        ]

        for candidate in candidates:
            if candidate is not None:
                return candidate

        return soup

    def _dedupe_chunks(
        self,
        chunks: List[str]
    ) -> List[str]:
        seen = set()
        deduped: List[str] = []

        for chunk in chunks:
            normalized = re.sub(r"\W+", "", chunk.lower())

            if not normalized:
                continue

            if normalized in seen:
                continue

            seen.add(normalized)
            deduped.append(chunk)

        return deduped

    def _extract_priority_text(
        self,
        root
    ) -> str:
        chunks: List[str] = []

        for tag in root.find_all(["h1", "h2", "h3", "p", "li", "blockquote"]):
            text = self._clean_text(
                tag.get_text(" ", strip=True)
            )

            if self._is_bad_content_chunk(text):
                continue

            chunks.append(text)

        chunks = self._dedupe_chunks(chunks)

        return " ".join(chunks)

    def _extract_block_text(
        self,
        root
    ) -> str:
        chunks: List[str] = []

        for tag in root.find_all(["p", "li", "h1", "h2", "h3", "blockquote"]):
            text = self._clean_text(
                tag.get_text(" ", strip=True)
            )

            if self._is_bad_content_chunk(text):
                continue

            chunks.append(text)

        chunks = self._dedupe_chunks(chunks)

        return " ".join(chunks)

    def _extract_fallback_text(
        self,
        soup: BeautifulSoup
    ) -> str:
        root = self._best_content_root(soup)

        return self._clean_text(
            root.get_text(" ", strip=True)
        )

    def _extract_main_text(
        self,
        soup: BeautifulSoup
    ) -> str:
        root = self._best_content_root(soup)

        priority_text = self._extract_priority_text(root)

        if len(priority_text) >= 200:
            return self._clean_text(priority_text)[: self.max_text_chars]

        block_text = self._extract_block_text(root)

        if len(block_text) >= 120:
            return self._clean_text(block_text)[: self.max_text_chars]

        fallback_text = self._extract_fallback_text(soup)

        return self._clean_text(fallback_text)[: self.max_text_chars]

    def extract(
        self,
        html: str,
        source_url: str = ""
    ) -> Dict[str, Any]:
        if not html:
            return {
                "status": "failed",
                "source_url": source_url,
                "page_title": "",
                "page_description": "",
                "page_text": "",
                "headings": [],
                "metadata": {},
                "raw_html": "",
                "error": "Empty HTML content",
            }

        try:
            soup = BeautifulSoup(html, "lxml")

            title = self._extract_title(soup)
            description = self._extract_description(soup)
            metadata = self._extract_metadata(soup)

            self._remove_noise(soup)

            headings = self._extract_headings(soup)
            page_text = self._extract_main_text(soup)

            return {
                "status": "success",
                "source_url": source_url,
                "page_title": title,
                "page_description": description,
                "page_text": page_text,
                "headings": headings,
                "metadata": metadata,
                "raw_html": html,
                "error": None,
            }

        except Exception as error:
            return {
                "status": "failed",
                "source_url": source_url,
                "page_title": "",
                "page_description": "",
                "page_text": "",
                "headings": [],
                "metadata": {},
                "raw_html": html,
                "error": str(error),
            }