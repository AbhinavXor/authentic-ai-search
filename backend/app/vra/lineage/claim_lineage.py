"""
=========================================================
MODULE: Claim Lineage Engine

Project:
Authentic AI Search

Purpose:
Trace claims back to supporting evidence.

Author:
Abhinav

Version:
1.0.0
=========================================================
"""

from typing import Any, Dict, List


class ClaimLineageEngine:
    """
    Build claim → source mapping.
    """

    def build(
        self,
        evidence_records: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:

        lineage = {}

        for record in evidence_records:

            claim = record.get(
                "extracted_claim"
            )

            if not claim:
                continue

            if claim not in lineage:
                lineage[claim] = []

            lineage[claim].append(
                {
                    "source": record.get(
                        "source_name"
                    ),

                    "domain": record.get(
                        "domain"
                    ),

                    "authority_score": record.get(
                        "authority_score",
                        0
                    ),

                    "reputation_score": record.get(
                        "reputation_score",
                        0
                    ),

                    "status": record.get(
                        "retrieval_status"
                    )
                }
            )

        results = []

        for claim, sources in lineage.items():

            results.append(
                {
                    "claim": claim,
                    "supporting_sources": sources,
                    "support_count": len(sources)
                }
            )

        return results