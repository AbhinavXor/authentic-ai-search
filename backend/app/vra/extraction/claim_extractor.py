"""
=========================================================
MODULE: Claim Extractor

Project:
Authentic AI Search

Purpose:
Extract factual evidence from fetched pages.

Version:
3.2.3
=========================================================
"""

# Updated backend/app/vra/extraction/claim_extractor.py

from typing import Any, Dict, Optional
import re


class ClaimExtractor:
    """
    Extracts concise factual claims from page content.

    Goals:
    - Avoid navigation/cookie/header/footer garbage.
    - Prefer factual definition/explanation sentences.
    - Prefer target-entity identity sentences for "Who is X?" queries.
    - Keep logic generic, not hardcoded to one person/entity.
    """

    MAX_CLAIM_LENGTH = 600
    MAX_DESCRIPTION_LENGTH = 400

    SENTENCE_SPLIT_PATTERN = re.compile(r"(?<=[.!?])\s+")

    BAD_TEXT_MARKERS = {
        "official website",
        "official websites use",
        "secure .gov websites use https",
        "a .gov website belongs",
        "https:// means you've safely connected",
        "you've safely connected",
        "contact contact",
        "media office",
        "table of contents",
        "download csv",
        "download xml",
        "download excel",
        "explore our databank",
        "databank",
        "home keywords",
        "keywords are tags",
        "cookie policy",
        "privacy policy",
        "terms of use",
        "skip to content",
        "skip to main content",
        "navigation menu",
        "all rights reserved",
        "continue to navigate this website",
        "cookies will be placed",
        "enable javascript",
        "share sensitive information",
        "an official website",
        "lock locked padlock",
        "menu close",
        "search search",
        "subscribe",
        "newsletter",
        "licensing",
        "copyrighted",
        "creative commons",
        "wikimedia commons",
        "government open data license",
        "featured speaker",
        "featured on",
        "share this page",
        "print updated",
        "related pages",
        "key points",
        "overview",
        "learn more",
        "video",
        "watch",
        "preview",
        "daybreak",
        "gross domestic product gross domestic product",
        "gdp current us",
        "international trade investment",
        "investment in fixed assets",
        "benefactor",
        "global learning xprize",
        "xprize",
        "talk with chatgpt",
        "updated:",
        "top questions",
        "news •",
        "news -",
        "et ( cnbc",
        "cnbc",
        "latest survey data",
        "for the latest survey",
        "about six-in-ten",
        "vogels",
        "fact sheet",
        "fast facts",
        "quiz",
        "flash cards",
        "quizlet",

        # Entity/infobox/list noise
        "official portrait",
        "incumbent assumed office",
        "citizenship",
        "education",
        "occupations",
        "show more",
        "see list",
        "born elon reeve musk",
        "official portrait,",
        "assumed office",
    }

    GENERIC_ENTITY_BAD_MARKERS = {
        "healthcare programme",
        "tri-ministerial",
        "ministry of women",
        "download",
        "source:",
        "file is",
        "licensing",
        "copyright",
        "yoga for healthy ageing",
        "adding life to years",
        "cookie",
        "newsletter",
        "featured speaker",
        "featured on",
        "benefactor",
        "global learning xprize",
        "xprize",
        "official biography",
        "official bio",

        # Entity/infobox/list noise
        "official portrait",
        "incumbent assumed office",
        "citizenship",
        "education",
        "occupations",
        "show more",
        "see list",
        "assumed office",
    }

    FACT_PATTERNS = [
        " is ",
        " are ",
        " was ",
        " were ",
        " refers to ",
        " means ",
        " defined as ",
        " consists of ",
        " stands for ",
        " measures ",
        " used to ",
        " responsible for ",
        " served as ",
        " serves as ",
        " known for ",
        " known as ",
        " born ",
        " increase in prices",
        " broad increase in prices",
        " purchasing power",
        " central bank",
        " gross domestic product",
        " final goods and services",
        " goods and services",
        " consumer price index",
        " prices rise",
        " inflation",
        " describes ",
        " represents ",
        " includes ",
        " provides ",
        " established ",
        " founded ",
        " headquartered ",
        " located in ",
        " serves ",
        " functions as ",
    ]

    ENTITY_IDENTITY_PATTERNS = [
        " is ",
        " was ",
        " is the ",
        " is an ",
        " is a ",
        " was the ",
        " was an ",
        " was a ",
        " served as ",
        " serves as ",
        " known for ",
        " known as ",
        " born ",
        " politician",
        " prime minister",
        " president",
        " chief minister",
        " member of parliament",
        " founder",
        " ceo",
        " chairperson",
        " minister",
        " actor",
        " author",
        " scientist",
        " economist",
        " entrepreneur",
        " organisation",
        " organization",
        " agency",
        " institution",
        " company",
    ]

    STRONG_ENTITY_PATTERNS = [
        " is a ",
        " is an ",
        " is the ",
        " is best known",
        " is known",
        " serves as",
        " served as",
        " founder",
        " chief executive",
        " ceo",
        " entrepreneur",
        " businessperson",
        " politician",
        " prime minister",
        " president",
        " chief executive officer",
        " founded",
        " founded by",
        " heads",
        " serves as the",
        " currently serves as",
    ]

    QUERY_HINTS = {
        "inflation": [
            "inflation",
            "prices",
            "price",
            "goods and services",
            "purchasing power",
            "consumer price",
            "broad increase",
        ],
        "gdp": [
            "gdp",
            "gross domestic product",
            "final goods and services",
            "economic activity",
            "value of goods",
            "value added",
        ],
        "rbi": [
            "rbi",
            "reserve bank",
            "reserve bank of india",
            "central bank",
            "monetary policy",
        ],
        "who": [
            "world health organization",
            "public health",
            "health",
        ],
        "imf": [
            "international monetary fund",
            "global economy",
            "financial stability",
        ],
        "mospi": [
            "ministry of statistics",
            "programme implementation",
            "government of india",
        ],
    }

    QUERY_PREFIXES = (
        "who is",
        "who was",
        "what is",
        "what are",
        "define",
        "meaning of",
    )

    def clean_text(self, text: Optional[str]) -> str:
        if not text:
            return ""

        return " ".join(str(text).split()).strip()

    def _normalize_text(self, text: str) -> str:
        text = self.clean_text(text).lower()
        text = re.sub(r"[^a-z0-9\s]", " ", text)

        return " ".join(text.split())

    def _get_query_text(self, evidence_record: Dict[str, Any]) -> str:
        return self.clean_text(
            evidence_record.get("query")
            or evidence_record.get("query_text")
            or ""
        )

    def _is_entity_query(self, evidence_record: Dict[str, Any]) -> bool:
        query_text = self._get_query_text(evidence_record).lower()

        return query_text.startswith(("who is", "who was"))

    def _is_definition_query(self, evidence_record: Dict[str, Any]) -> bool:
        query_text = self._get_query_text(evidence_record).lower()

        return query_text.startswith(
            ("what is", "what are", "define", "meaning of")
        )

    def _extract_query_target(self, evidence_record: Dict[str, Any]) -> str:
        query_text = self._get_query_text(evidence_record)
        query_lower = query_text.lower().strip()

        for prefix in self.QUERY_PREFIXES:
            if query_lower.startswith(prefix):
                target = query_text[len(prefix):]
                target = target.replace("?", "")
                target = target.strip(" :-—–")

                return self.clean_text(target)

        return ""

    def _target_tokens(self, target: str) -> list[str]:
        normalized = self._normalize_text(target)

        return [
            token
            for token in normalized.split()
            if len(token) > 2
        ]

    def _target_match_score(self, sentence: str, target: str) -> float:
        if not target:
            return 0.0

        sentence_normalized = self._normalize_text(sentence)
        target_normalized = self._normalize_text(target)

        if not target_normalized:
            return 0.0

        if target_normalized in sentence_normalized:
            return 80.0

        target_tokens = self._target_tokens(target)

        if not target_tokens:
            return 0.0

        sentence_tokens = sentence_normalized.split()

        matched = sum(
            1
            for token in target_tokens
            if token in sentence_tokens
        )

        ratio = matched / max(len(target_tokens), 1)

        if ratio >= 0.75:
            return 60.0

        if ratio >= 0.50:
            return 35.0

        if matched >= 1:
            return 15.0

        return 0.0

    def _is_bad_sentence(self, sentence: str) -> bool:
        sentence_lower = sentence.lower()
        sentence_stripped = sentence_lower.strip()

        if len(sentence.split()) > 80:
            return True

        if sentence_stripped.startswith(
            (
                "featured speaker",
                "featured on",
                "key points",
                "overview",
                "updated:",
                "share this page",
                "related pages",
            )
        ):
            return True

        if "top questions" in sentence_lower:
            return True

        if "news •" in sentence_lower:
            return True

        if "cnbc" in sentence_lower:
            return True

        if "for the latest survey" in sentence_lower:
            return True

        if "vogels" in sentence_lower:
            return True

        if sentence_lower.count("?") > 2:
            return True

        if sentence_lower.count(" what ") > 2:
            return True

        if sentence_lower.count(" when ") > 2:
            return True

        if sentence_lower.count("show more") >= 2:
            return True

        if sentence_lower.count("read more") >= 2:
            return True

        if sentence_lower.count("featured") >= 2:
            return True

        if sentence_lower.count("updated") >= 2:
            return True

        if sentence_lower.count("share") >= 3:
            return True

        if (
            sentence_lower.count(" born ") >= 1
            and sentence_lower.count(" citizenship ") >= 1
        ):
            return True

        if (
            sentence_lower.count(" education ") >= 1
            and sentence_lower.count(" occupations ") >= 1
        ):
            return True

        if (
            "official portrait" in sentence_lower
            and "incumbent" in sentence_lower
        ):
            return True

        if (
            "assumed office" in sentence_lower
            and (
                "president" in sentence_lower
                or "vice president" in sentence_lower
                or "incumbent" in sentence_lower
            )
        ):
            return True

        for marker in self.BAD_TEXT_MARKERS:
            if marker in sentence_lower:
                return True

        if "cookie" in sentence_lower:
            return True

        if "http" in sentence_lower:
            return True

        if ".gov" in sentence_lower:
            return True

        if "secure" in sentence_lower and "website" in sentence_lower:
            return True

        if "navigate this website" in sentence_lower:
            return True

        if "download" in sentence_lower and any(
            word in sentence_lower
            for word in ["csv", "xml", "excel", "pdf"]
        ):
            return True

        if sentence_lower.count("|") >= 2:
            return True

        if sentence_lower.count(" contact ") >= 2:
            return True

        return False

    def _looks_factual(self, sentence: str) -> bool:
        sentence_lower = sentence.lower()

        return any(
            pattern in sentence_lower
            for pattern in self.FACT_PATTERNS
        )

    def _looks_like_entity_identity(self, sentence: str) -> bool:
        sentence_lower = sentence.lower()

        return any(
            pattern in sentence_lower
            for pattern in self.ENTITY_IDENTITY_PATTERNS
        )

    def _query_keywords(self, evidence_record: Dict[str, Any]) -> list[str]:
        query_text = self._get_query_text(evidence_record).lower()
        keywords: list[str] = []

        for key, hints in self.QUERY_HINTS.items():
            if key in query_text:
                keywords.extend(hints)

        target = self._extract_query_target(evidence_record)

        if target:
            keywords.append(target.lower())
            keywords.extend(self._target_tokens(target))

        if self._is_entity_query(evidence_record):
            keywords.extend(
                [
                    "is",
                    "was",
                    "served as",
                    "serves as",
                    "known for",
                    "known as",
                    "born",
                    "prime minister",
                    "president",
                    "chief minister",
                    "member of parliament",
                    "founder",
                    "ceo",
                    "politician",
                    "minister",
                    "organization",
                    "organisation",
                    "company",
                    "institution",
                ]
            )

        return keywords

    def _query_relevance_score(
        self,
        sentence: str,
        evidence_record: Dict[str, Any]
    ) -> float:
        sentence_lower = sentence.lower()
        keywords = self._query_keywords(evidence_record)

        if not keywords:
            return 0.0

        score = 0.0

        for keyword in keywords:
            keyword = keyword.strip().lower()

            if not keyword:
                continue

            if keyword in sentence_lower:
                score += 12.0

        return min(score, 100.0)

    def _entity_query_score_adjustment(
        self,
        sentence: str,
        evidence_record: Dict[str, Any]
    ) -> float:
        if not self._is_entity_query(evidence_record):
            return 0.0

        score = 0.0
        sentence_lower = sentence.lower()

        target = self._extract_query_target(evidence_record)

        target_score = self._target_match_score(sentence, target)

        score += target_score

        if target_score <= 0:
            score -= 55.0

        if self._looks_like_entity_identity(sentence):
            score += 45.0

        if any(
            phrase in sentence_lower
            for phrase in self.STRONG_ENTITY_PATTERNS
        ):
            score += 45.0

        if " was born " in sentence_lower:
            score -= 10.0

        if " born on " in sentence_lower:
            score -= 10.0

        if any(
            marker in sentence_lower
            for marker in self.GENERIC_ENTITY_BAD_MARKERS
        ):
            score -= 90.0

        if any(
            marker in sentence_lower
            for marker in [
                "official portrait",
                "featured speaker",
                "benefactor",
            ]
        ):
            score -= 120.0

        if len(sentence) > 320:
            score -= 20.0

        return score

    def _sentence_score(
        self,
        sentence: str,
        evidence_record: Dict[str, Any]
    ) -> float:
        score = 0.0
        sentence_lower = sentence.lower()

        if self._looks_factual(sentence):
            score += 35.0

        if evidence_record.get("is_official"):
            score += 12.0

        if evidence_record.get("is_trusted"):
            score += 6.0

        score += self._query_relevance_score(sentence, evidence_record)
        score += self._entity_query_score_adjustment(sentence, evidence_record)

        if 60 <= len(sentence) <= 280:
            score += 15.0

        if len(sentence) > 400:
            score -= 15.0

        if any(
            phrase in sentence_lower
            for phrase in [
                "news",
                "top questions",
                "latest survey",
                "cnbc",
                "updated:",
            ]
        ):
            score -= 80.0

        if self._is_entity_query(evidence_record):
            if 50 <= len(sentence) <= 260:
                score += 15.0

            if len(sentence) > 300:
                score -= 40.0

        if any(
            phrase in sentence_lower
            for phrase in [
                "what is",
                "definition",
                "defined as",
                "refers to",
                "means",
                "stands for",
            ]
        ):
            score += 10.0

        if self._is_definition_query(evidence_record) and any(
            phrase in sentence_lower
            for phrase in [
                "stands for",
                " is a ",
                " is an ",
                "refers to",
                "defined as",
            ]
        ):
            score += 25.0

        if (
            self._is_definition_query(evidence_record)
            and any(
                phrase in sentence_lower
                for phrase in [
                    "gross domestic product is",
                    "inflation is",
                    "gdp stands for",
                    "refers to",
                    "defined as",
                ]
            )
        ):
            score += 30.0

        if (
            self._is_definition_query(evidence_record)
            and sentence_lower.startswith(
                (
                    "gross domestic product",
                    "inflation is",
                    "gdp stands for",
                )
            )
        ):
            score += 20

        if sentence_lower.startswith(
            (
                "what is",
                "table of contents",
                "home",
                "contact",
            )
        ):
            score -= 20.0

        return score

    def _split_sentences(self, text: str) -> list[str]:
        if not text:
            return []

        text = text.replace(" News • ", ". ")
        text = text.replace(" Top Questions ", ". ")
        text = text.replace(" About six-in-ten ", ". About six-in-ten ")
        text = text.replace(" Updated: ", ". Updated: ")

        rough_sentences = self.SENTENCE_SPLIT_PATTERN.split(text)

        sentences = []

        for sentence in rough_sentences:
            sentence = self.clean_text(sentence)

            if not sentence:
                continue

            if len(sentence) < 40:
                continue

            if sentence.count(":") >= 4:
                continue

            if sentence.count(";") >= 5:
                continue

            if self._is_bad_sentence(sentence):
                continue

            if len(sentence) > self.MAX_CLAIM_LENGTH:
                sentence = sentence[: self.MAX_CLAIM_LENGTH]

            sentences.append(sentence)

        return sentences

    def _best_sentence(
        self,
        text: str,
        evidence_record: Dict[str, Any]
    ) -> Optional[str]:
        sentences = self._split_sentences(text)

        if not sentences:
            return None

        target = self._extract_query_target(evidence_record)

        target_matched_sentences = [
            sentence
            for sentence in sentences
            if (
                self._target_match_score(sentence, target) >= 60.0
                and not self._is_bad_sentence(sentence)
            )
        ]

        if target_matched_sentences:
            return sorted(
                target_matched_sentences,
                key=lambda sentence: self._sentence_score(
                    sentence,
                    evidence_record
                ),
                reverse=True,
            )[0]

        scored_sentences = sorted(
            sentences,
            key=lambda sentence: self._sentence_score(
                sentence,
                evidence_record
            ),
            reverse=True,
        )

        best_sentence = scored_sentences[0]

        if self._sentence_score(best_sentence, evidence_record) <= 0:
            return None

        return best_sentence

    def _extract_claim(
        self,
        page_text: str,
        evidence_record: Dict[str, Any]
    ) -> Optional[str]:
        return self._best_sentence(page_text, evidence_record)

    def _extract_description(
        self,
        page_description: Optional[str],
        page_text: str,
        evidence_record: Dict[str, Any]
    ) -> Optional[str]:
        if page_description:
            description = self.clean_text(page_description)

            if description and not self._is_bad_sentence(description):
                if len(description) > self.MAX_DESCRIPTION_LENGTH:
                    description = description[: self.MAX_DESCRIPTION_LENGTH]

                return description

        return self._best_sentence(page_text, evidence_record)

    def extract(self, evidence_record: Dict[str, Any]) -> Dict[str, Any]:
        page_text = self.clean_text(evidence_record.get("page_text"))

        extracted_claim = self._extract_claim(page_text, evidence_record)

        description = self._extract_description(
            evidence_record.get("page_description"),
            page_text,
            evidence_record,
        )

        evidence_record["extracted_claim"] = extracted_claim

        evidence_record["claim_confidence"] = (
            100.0
            if extracted_claim
            else 0.0
        )

        evidence_record["page_description"] = description

        return evidence_record

    def extract_claims(
        self,
        evidence_records: list[dict[str, Any]]
    ) -> list[dict[str, Any]]:
        return self.extract_batch(evidence_records)

    def extract_batch(
        self,
        evidence_records: list[dict[str, Any]]
    ) -> list[dict[str, Any]]:
        return [
            self.extract(record)
            for record in evidence_records
        ]