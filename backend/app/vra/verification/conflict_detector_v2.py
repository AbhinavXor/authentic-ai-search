"""
=========================================================
MODULE: Conflict Detector V2

Project:
Authentic AI Search

Engine:
VRA Search Engine

Purpose:
Detect possible conflicts, contradictions, or mismatches
between extracted claims from multiple sources.

Author:
Abhinav

Version:
1.0.0
=========================================================
"""

import re
from typing import Any, Dict, List, Set


class ConflictDetectorV2:
    """
    Rule-based conflict detector for evidence claims.

    This module is intentionally independent.
    It will be integrated into pipeline.py later.
    """

    def __init__(self) -> None:
        self.negation_terms = {
            "not",
            "no",
            "never",
            "false",
            "incorrect",
            "denied",
            "does not",
            "do not",
            "is not",
            "are not",
            "was not",
            "were not"
        }

    def _normalize(
        self,
        text: str
    ) -> str:
        """
        Normalize claim text.
        """

        if not text:
            return ""

        text = text.lower().strip()

        text = re.sub(
            r"[^a-z0-9\s.%/-]",
            "",
            text
        )

        text = re.sub(
            r"\s+",
            " ",
            text
        )

        return text.strip()

    def _tokens(
        self,
        text: str
    ) -> Set[str]:
        """
        Convert text into token set.
        """

        normalized = self._normalize(text)

        return {
            token
            for token in normalized.split()
            if len(token) > 2
        }

    def _similarity(
        self,
        first: str,
        second: str
    ) -> float:
        """
        Calculate simple Jaccard similarity.
        """

        first_tokens = self._tokens(first)
        second_tokens = self._tokens(second)

        if not first_tokens or not second_tokens:
            return 0.0

        intersection = first_tokens.intersection(second_tokens)
        union = first_tokens.union(second_tokens)

        return len(intersection) / len(union)

    def _has_negation(
        self,
        text: str
    ) -> bool:
        """
        Detect negation terms.
        """

        normalized = self._normalize(text)

        return any(
            term in normalized
            for term in self.negation_terms
        )

    def _extract_numbers(
        self,
        text: str
    ) -> List[str]:
        """
        Extract numeric values from text.
        """

        if not text:
            return []

        return re.findall(
            r"\b\d+(?:\.\d+)?%?\b",
            text
        )

    def compare_claims(
        self,
        first_claim: str,
        second_claim: str
    ) -> Dict[str, Any]:
        """
        Compare two claims.
        """

        similarity = self._similarity(
            first_claim,
            second_claim
        )

        first_has_negation = self._has_negation(
            first_claim
        )

        second_has_negation = self._has_negation(
            second_claim
        )

        first_numbers = self._extract_numbers(
            first_claim
        )

        second_numbers = self._extract_numbers(
            second_claim
        )

        conflict_reasons = []

        if similarity >= 0.35 and first_has_negation != second_has_negation:
            conflict_reasons.append(
                "similar_claim_with_negation_difference"
            )

        if (
            similarity >= 0.25
            and first_numbers
            and second_numbers
            and first_numbers != second_numbers
        ):
            conflict_reasons.append(
                "similar_claim_with_different_numbers"
            )

        status = (
            "possible_conflict"
            if conflict_reasons
            else "no_conflict"
        )

        return {
            "status": status,
            "similarity": round(similarity, 3),
            "reasons": conflict_reasons,
            "first_numbers": first_numbers,
            "second_numbers": second_numbers
        }

    def detect(
        self,
        evidence_records: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Detect conflicts across evidence records.
        """

        successful_records = [
            record
            for record in evidence_records
            if record.get("retrieval_status") == "success"
            and record.get("extracted_claim")
        ]

        conflicts = []

        for first_index in range(len(successful_records)):
            for second_index in range(
                first_index + 1,
                len(successful_records)
            ):
                first_record = successful_records[first_index]
                second_record = successful_records[second_index]

                comparison = self.compare_claims(
                    first_claim=first_record.get(
                        "extracted_claim",
                        ""
                    ),
                    second_claim=second_record.get(
                        "extracted_claim",
                        ""
                    )
                )

                if comparison.get("status") == "possible_conflict":
                    conflicts.append(
                        {
                            "first_source": first_record.get(
                                "source_name"
                            ),
                            "second_source": second_record.get(
                                "source_name"
                            ),
                            "first_domain": first_record.get(
                                "domain"
                            ),
                            "second_domain": second_record.get(
                                "domain"
                            ),
                            "first_claim": first_record.get(
                                "extracted_claim"
                            ),
                            "second_claim": second_record.get(
                                "extracted_claim"
                            ),
                            "similarity": comparison.get(
                                "similarity"
                            ),
                            "reasons": comparison.get(
                                "reasons"
                            )
                        }
                    )

        return {
            "conflict_status": (
                "conflict_detected"
                if conflicts
                else "no_conflict_detected"
            ),
            "conflict_count": len(conflicts),
            "conflicts": conflicts
        }