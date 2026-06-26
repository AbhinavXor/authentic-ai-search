"""
=========================================================
MODULE: Consensus Engine

Project:
Authentic AI Search

Purpose:
Build consensus from extracted verified evidence.

Version:
3.1.0
=========================================================
"""

import re
from typing import Any, Dict, List, Set


class ConsensusEngine:
    """
    Evidence consensus engine.

    Groups semantically similar factual claims using lightweight
    token similarity so equivalent claims with different wording
    do not become false mixed_evidence.
    """

    STOP_WORDS = {
        "a", "an", "the", "is", "are", "was", "were", "be", "been",
        "being", "of", "for", "to", "in", "on", "at", "by", "with",
        "from", "as", "and", "or", "that", "this", "these", "those",
        "it", "its", "into", "during", "over", "time", "also",
        "based", "limited", "verified", "evidence",
    }

    SYNONYMS = {
        "gdp": "gross domestic product",
        "gross domestic product": "gross domestic product",
        "rbi": "reserve bank india",
        "reserve bank of india": "reserve bank india",
        "who": "world health organization",
        "imf": "international monetary fund",
        "mospi": "ministry statistics programme implementation",
    }

    def _safe_float(
        self,
        value: Any,
        default: float = 0.0
    ) -> float:
        try:
            if value is None:
                return default

            return float(value)

        except Exception:
            return default

    def _clean_text(
        self,
        text: str
    ) -> str:
        text = text.lower()

        for key, value in self.SYNONYMS.items():
            text = text.replace(key, value)

        text = re.sub(r"[^a-z0-9\s]", " ", text)

        return " ".join(text.split())

    def _tokens(
        self,
        text: str
    ) -> Set[str]:
        cleaned = self._clean_text(text)

        return {
            token
            for token in cleaned.split()
            if len(token) > 2 and token not in self.STOP_WORDS
        }

    def _claim_similarity(
        self,
        claim_a: str,
        claim_b: str
    ) -> float:
        tokens_a = self._tokens(claim_a)
        tokens_b = self._tokens(claim_b)

        if not tokens_a or not tokens_b:
            return 0.0

        overlap = len(tokens_a.intersection(tokens_b))
        union = len(tokens_a.union(tokens_b))

        jaccard = overlap / max(union, 1)

        containment = max(
            overlap / max(len(tokens_a), 1),
            overlap / max(len(tokens_b), 1),
        )

        return round(
            (jaccard * 0.45) + (containment * 0.55),
            4
        )

    def _is_similar_claim(
        self,
        claim_a: str,
        claim_b: str
    ) -> bool:
        similarity = self._claim_similarity(
            claim_a,
            claim_b
        )

        if similarity >= 0.42:
            return True

        tokens_a = self._tokens(claim_a)
        tokens_b = self._tokens(claim_b)

        important_overlap = tokens_a.intersection(tokens_b)

        if len(important_overlap) >= 3:
            return True

        return False

    def _record_weight(
        self,
        record: Dict[str, Any]
    ) -> float:
        authority = self._safe_float(
            record.get("authority_score"),
            0
        )
        relevance = self._safe_float(
            record.get("relevance_score"),
            50
        )
        rank = self._safe_float(
            record.get("rank_score"),
            50
        )
        official_confidence = self._safe_float(
            record.get("official_confidence_score"),
            authority,
        )

        weight = (
            authority * 0.35
            + relevance * 0.20
            + rank * 0.20
            + official_confidence * 0.25
        )

        if record.get("is_official"):
            weight += 8

        if record.get("is_trusted"):
            weight += 5

        if record.get("can_support_verified_answer") is False:
            weight -= 15

        return round(
            max(0.0, min(weight, 100.0)),
            2
        )

    def _find_matching_group(
        self,
        claim: str,
        claim_groups: List[Dict[str, Any]]
    ) -> Dict[str, Any] | None:
        best_group = None
        best_similarity = 0.0

        for group in claim_groups:
            representative_claim = group["representative_claim"]

            similarity = self._claim_similarity(
                claim,
                representative_claim
            )

            if similarity > best_similarity:
                best_similarity = similarity
                best_group = group

        if best_group and (
            best_similarity >= 0.42
            or self._is_similar_claim(
                claim,
                best_group["representative_claim"]
            )
        ):
            return best_group

        return None

    def _calculate_agreement_score(
        self,
        claim_groups: List[Dict[str, Any]],
        total_claims: int
    ) -> float:
        if total_claims <= 0 or not claim_groups:
            return 0.0

        best_group = max(
            claim_groups,
            key=lambda group: (
                group["support_count"],
                group["total_weight"],
            ),
        )

        total_weight = sum(
            group["total_weight"]
            for group in claim_groups
        )

        support_ratio = best_group["support_count"] / total_claims
        weight_ratio = best_group["total_weight"] / max(
            total_weight,
            1
        )

        agreement_score = (
            support_ratio * 55
            + weight_ratio * 45
        )

        if best_group["support_count"] == total_claims:
            agreement_score = max(
                agreement_score,
                95.0
            )

        if best_group["support_count"] >= 2 and support_ratio >= 0.5:
            agreement_score = max(
                agreement_score,
                75.0
            )

        if best_group["support_count"] == 1 and total_claims == 1:
            agreement_score = 100.0

        return round(
            max(0.0, min(agreement_score, 100.0)),
            2
        )

    def _determine_consensus_status(
        self,
        agreement_score: float,
        total_claims: int,
        unique_claim_count: int
    ) -> str:
        if total_claims == 0:
            return "insufficient_evidence"

        if total_claims == 1:
            return "high_agreement"

        if agreement_score >= 80:
            return "high_agreement"

        if agreement_score >= 55:
            return "moderate_agreement"

        if unique_claim_count > 1:
            return "mixed_evidence"

        return "insufficient_evidence"

    def generate(
        self,
        evidence_records: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        claim_groups: List[Dict[str, Any]] = []
        claims: List[str] = []

        for record in evidence_records:
            if record.get("retrieval_status") != "success":
                continue

            claim = (
                record.get("extracted_claim")
                or record.get("primary_claim")
            )

            if not isinstance(claim, str) or not claim.strip():
                continue

            claim = claim.strip()
            weight = self._record_weight(record)
            claims.append(claim)

            matching_group = self._find_matching_group(
                claim,
                claim_groups
            )

            if matching_group is None:
                matching_group = {
                    "representative_claim": claim,
                    "claims": [],
                    "sources": [],
                    "support_count": 0,
                    "total_weight": 0.0,
                    "average_weight": 0.0,
                }
                claim_groups.append(matching_group)

            matching_group["claims"].append(claim)
            matching_group["support_count"] += 1
            matching_group["total_weight"] += weight
            matching_group["sources"].append(
                {
                    "source": record.get("source_name"),
                    "domain": record.get("domain"),
                    "url": record.get("source_url"),
                    "authority_score": record.get(
                        "authority_score",
                        0
                    ),
                    "rank_score": record.get(
                        "rank_score",
                        0
                    ),
                    "is_official": record.get(
                        "is_official",
                        False
                    ),
                    "is_trusted": record.get(
                        "is_trusted",
                        False
                    ),
                }
            )

        for group in claim_groups:
            group["average_weight"] = round(
                group["total_weight"]
                / max(group["support_count"], 1),
                2,
            )
            group["total_weight"] = round(
                group["total_weight"],
                2
            )

        total_claims = len(claims)
        unique_claim_count = len(claim_groups)

        ranked_groups = sorted(
            claim_groups,
            key=lambda group: (
                group["support_count"],
                group["total_weight"],
                group["average_weight"],
            ),
            reverse=True,
        )

        agreement_score = self._calculate_agreement_score(
            claim_groups=ranked_groups,
            total_claims=total_claims,
        )

        consensus_status = self._determine_consensus_status(
            agreement_score=agreement_score,
            total_claims=total_claims,
            unique_claim_count=unique_claim_count,
        )

        consensus_text = ""

        if ranked_groups:
            consensus_text = ranked_groups[0]["representative_claim"]

        return {
            "consensus": consensus_text,
            "consensus_answer": consensus_text,
            "agreement_score": agreement_score,
            "consensus_status": consensus_status,
            "claim_count": total_claims,
            "unique_claim_count": unique_claim_count,
            "claim_groups": ranked_groups,
            "ranked_claims": ranked_groups[:10],
        }