"""
=========================================================
MODULE: Claim Similarity Engine

Project:
Authentic AI Search

Engine:
Verified Resource Algorithm (VRA)

Purpose:
Group semantically similar claims to reduce false contradictions.

Author:
Abhinav

Version:
1.0.0
=========================================================
"""

import re
from typing import Any, Dict, List


class ClaimSimilarityEngine:
    """
    Groups similar claims using normalized lexical overlap.

    MVP:
    - Lowercase
    - Remove punctuation
    - Remove common words
    - Compare token overlap

    Future:
    - Embeddings
    - Sentence similarity
    - NLI contradiction detection
    """

    def __init__(self) -> None:
        self.stopwords = {
            "the",
            "a",
            "an",
            "is",
            "are",
            "was",
            "were",
            "for",
            "of",
            "and",
            "or",
            "to",
            "in",
            "on",
            "by",
            "with",
            "from",
            "as",
            "it",
            "this",
            "that"
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

        text = text.lower()

        text = re.sub(
            r"[^a-z0-9\s]",
            " ",
            text
        )

        words = [
            word
            for word in text.split()
            if word not in self.stopwords
        ]

        return " ".join(words)

    def _similarity(
        self,
        claim_a: str,
        claim_b: str
    ) -> float:
        """
        Calculate simple token overlap similarity.
        """

        norm_a = self._normalize(claim_a)
        norm_b = self._normalize(claim_b)

        tokens_a = set(norm_a.split())
        tokens_b = set(norm_b.split())

        if not tokens_a or not tokens_b:
            return 0.0

        overlap = tokens_a.intersection(tokens_b)
        union = tokens_a.union(tokens_b)

        score = len(overlap) / len(union)

        return round(score * 100, 2)

    def group_claims(
        self,
        evidence_records: List[Dict[str, Any]],
        threshold: float = 60.0
    ) -> List[Dict[str, Any]]:
        """
        Group similar extracted claims.
        """

        groups: List[Dict[str, Any]] = []

        for record in evidence_records:
            claim = record.get("extracted_claim")

            if not claim:
                continue

            claim = claim.strip()

            matched_group = None

            for group in groups:
                similarity = self._similarity(
                    claim,
                    group["representative_claim"]
                )

                if similarity >= threshold:
                    matched_group = group
                    break

            if matched_group:
                matched_group["claims"].append(claim)
                matched_group["sources"].append(
                    {
                        "source": record.get("source_name"),
                        "domain": record.get("domain"),
                        "authority_score": record.get(
                            "authority_score",
                            0
                        )
                    }
                )
                matched_group["support_count"] += 1

            else:
                groups.append(
                    {
                        "representative_claim": claim,
                        "claims": [claim],
                        "sources": [
                            {
                                "source": record.get("source_name"),
                                "domain": record.get("domain"),
                                "authority_score": record.get(
                                    "authority_score",
                                    0
                                )
                            }
                        ],
                        "support_count": 1
                    }
                )

        groups = sorted(
            groups,
            key=lambda group: group.get("support_count", 0),
            reverse=True
        )

        return groups