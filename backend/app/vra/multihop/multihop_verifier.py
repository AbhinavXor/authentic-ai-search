"""
=========================================================
MODULE: Multi-Hop Verification Engine

Project:
Authentic AI Search

Engine:
Verified Resource Algorithm (VRA)

Purpose:
Build evidence chains between claims.

Author:
Abhinav

Version:
1.0.0
=========================================================
"""

from typing import Any, Dict, List


class MultiHopVerifier:
    """
    Build evidence chains across claims.
    """

    def build(
        self,
        evidence_records: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:

        chains = []

        verified_claims = []

        for record in evidence_records:

            claim = record.get(
                "extracted_claim"
            )

            if not claim:
                continue

            verified_claims.append(
                {
                    "claim": claim,
                    "source": record.get(
                        "source_name"
                    ),
                    "domain": record.get(
                        "domain"
                    ),
                    "authority_score": record.get(
                        "authority_score",
                        0
                    )
                }
            )

        for i, claim in enumerate(
            verified_claims
        ):

            chains.append(
                {
                    "hop_id": i + 1,
                    "claim": claim["claim"],
                    "source": claim["source"],
                    "domain": claim["domain"],
                    "authority_score":
                    claim["authority_score"]
                }
            )

        return chains