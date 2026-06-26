"""
=========================================================
MODULE: Evidence Cluster Engine

Project:
Authentic AI Search

Engine:
Verified Resource Algorithm (VRA)

Purpose:
Cluster evidence records by claim.

Author:
Abhinav

Version:
1.0.0
=========================================================
"""

from typing import Any, Dict, List


class EvidenceClusterEngine:
    """
    Cluster evidence around claims.
    """

    def build(
        self,
        evidence_records: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:

        clusters = {}

        for record in evidence_records:

            claim = record.get(
                "extracted_claim"
            )

            if not claim:
                continue

            claim = claim.strip()

            if claim not in clusters:

                clusters[claim] = {
                    "claim": claim,
                    "support_count": 0,
                    "sources": []
                }

            clusters[claim]["support_count"] += 1

            clusters[claim]["sources"].append(
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
                    "status": record.get(
                        "retrieval_status"
                    )
                }
            )

        cluster_list = list(
            clusters.values()
        )

        cluster_list.sort(
            key=lambda cluster:
            cluster["support_count"],
            reverse=True
        )

        return cluster_list