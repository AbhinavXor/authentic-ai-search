"""
=========================================================
MODULE: Evidence Synthesizer
=========================================================
"""

from typing import Any, Dict, List


class EvidenceSynthesizer:
    """
    Builds a synthesized answer from extracted claims.
    """

    def synthesize(
        self,
        evidence_records: List[Dict[str, Any]]
    ) -> str:

        claims = []

        for record in evidence_records:

            claim = record.get("extracted_claim")

            if claim:
                claims.append(claim)

        if not claims:
            return (
                "No verified evidence could be synthesized "
                "from the selected trusted sources."
            )

        return " | ".join(claims[:3])