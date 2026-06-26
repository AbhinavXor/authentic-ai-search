"""
=========================================================
MODULE: Contradiction Detector

Project:
Authentic AI Search

Purpose:
Detect strong contradictions between extracted claims.

Version:
2.1.0
=========================================================
"""

import re
from typing import Any, Dict, List


class ContradictionDetector:
    """
    Conservative contradiction detector.

    Goal:
    - Avoid false contradiction from normal explanatory variation.
    - Avoid treating different dates/numbers on broad topic pages as contradictions.
    - Detect only strong negation, numeric, or year conflicts when claims are highly similar.
    """

    NEGATION_TERMS = {
        "not",
        "no",
        "never",
        "cannot",
        "can't",
        "does not",
        "do not",
        "is not",
        "are not",
        "was not",
        "were not",
        "isn't",
        "aren't",
        "wasn't",
        "weren't",
    }

    SOFT_VARIATION_TERMS = {
        "some",
        "may",
        "can",
        "could",
        "often",
        "usually",
        "generally",
        "broad",
        "overall",
        "headline",
        "core",
        "annual",
        "monthly",
        "quarterly",
        "consumer price",
        "producer price",
        "index",
        "database",
        "measure",
        "measures",
    }

    def _normalize(
        self,
        text: str
    ) -> str:
        return " ".join(
            (text or "")
            .lower()
            .replace("’", "'")
            .replace("“", '"')
            .replace("”", '"')
            .split()
        )

    def _extract_numbers(
        self,
        text: str
    ) -> List[str]:
        return re.findall(
            r"\b\d+(?:\.\d+)?\s*(?:%|percent|million|billion|trillion|crore|lakh)?\b",
            text.lower(),
        )

    def _extract_years(
        self,
        text: str
    ) -> List[str]:
        return re.findall(
            r"\b(?:19|20)\d{2}\b",
            text
        )

    def _has_negation(
        self,
        text: str
    ) -> bool:
        normalized = self._normalize(text)

        return any(
            term in normalized
            for term in self.NEGATION_TERMS
        )

    def _has_soft_variation(
        self,
        text: str
    ) -> bool:
        normalized = self._normalize(text)

        return any(
            term in normalized
            for term in self.SOFT_VARIATION_TERMS
        )

    def _token_set(
        self,
        text: str
    ) -> set[str]:
        normalized = re.sub(
            r"[^a-z0-9\s]",
            " ",
            self._normalize(text)
        )

        stop_words = {
            "the", "a", "an", "is", "are", "was", "were",
            "of", "to", "in", "on", "for", "and", "or",
            "by", "with", "from", "that", "this", "it",
            "as", "be", "has", "have", "had", "their",
            "its", "into", "over", "time",
        }

        return {
            token
            for token in normalized.split()
            if len(token) > 2 and token not in stop_words
        }

    def _similarity(
        self,
        left: str,
        right: str
    ) -> float:
        left_tokens = self._token_set(left)
        right_tokens = self._token_set(right)

        if not left_tokens or not right_tokens:
            return 0.0

        intersection = left_tokens.intersection(right_tokens)
        union = left_tokens.union(right_tokens)

        return len(intersection) / max(len(union), 1)

    def _numeric_conflict(
        self,
        left: str,
        right: str
    ) -> bool:
        left_numbers = self._extract_numbers(left)
        right_numbers = self._extract_numbers(right)

        if not left_numbers or not right_numbers:
            return False

        similarity = self._similarity(left, right)

        # Very conservative: numeric differences only conflict when
        # the claims are almost the same claim.
        if similarity < 0.75:
            return False

        if self._has_soft_variation(left) or self._has_soft_variation(right):
            return False

        return set(left_numbers) != set(right_numbers)

    def _year_conflict(
        self,
        left: str,
        right: str
    ) -> bool:
        left_years = self._extract_years(left)
        right_years = self._extract_years(right)

        if not left_years or not right_years:
            return False

        similarity = self._similarity(left, right)

        # Different years on broad pages are usually different facts,
        # not contradictions.
        if similarity < 0.75:
            return False

        if self._has_soft_variation(left) or self._has_soft_variation(right):
            return False

        return set(left_years) != set(right_years)

    def _negation_conflict(
        self,
        left: str,
        right: str
    ) -> bool:
        similarity = self._similarity(left, right)

        if similarity < 0.55:
            return False

        return self._has_negation(left) != self._has_negation(right)

    def _pair_conflict(
        self,
        left: str,
        right: str
    ) -> Dict[str, Any]:
        reasons = []

        if self._negation_conflict(left, right):
            reasons.append("negation_conflict")

        if self._numeric_conflict(left, right):
            reasons.append("numeric_conflict")

        if self._year_conflict(left, right):
            reasons.append("year_conflict")

        similarity = self._similarity(left, right)

        confidence = 0.0

        if reasons:
            confidence = min(
                1.0,
                0.40 + (len(reasons) * 0.20) + (similarity * 0.20)
            )

        return {
            "conflict": bool(reasons),
            "confidence": round(confidence, 2),
            "similarity": round(similarity, 2),
            "reasons": reasons,
            "left_claim": left,
            "right_claim": right,
        }

    def detect(
        self,
        claims: List[str]
    ) -> Dict[str, Any]:
        clean_claims = [
            claim.strip()
            for claim in claims
            if isinstance(claim, str) and claim.strip()
        ]

        if len(clean_claims) < 2:
            return {
                "contradiction": False,
                "confidence": 0.0,
                "conflict_count": 0,
                "conflicts": [],
            }

        conflicts = []

        for left_index in range(len(clean_claims)):
            for right_index in range(left_index + 1, len(clean_claims)):
                result = self._pair_conflict(
                    clean_claims[left_index],
                    clean_claims[right_index],
                )

                if result["conflict"]:
                    conflicts.append(result)

        if not conflicts:
            return {
                "contradiction": False,
                "confidence": 0.0,
                "conflict_count": 0,
                "conflicts": [],
            }

        max_confidence = max(
            conflict["confidence"]
            for conflict in conflicts
        )

        strong_conflicts = [
            conflict
            for conflict in conflicts
            if conflict["confidence"] >= 0.75
        ]

        return {
            "contradiction": bool(strong_conflicts),
            "confidence": max_confidence,
            "conflict_count": len(conflicts),
            "strong_conflict_count": len(strong_conflicts),
            "conflicts": conflicts,
        }