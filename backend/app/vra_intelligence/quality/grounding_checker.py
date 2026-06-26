"""
=========================================================
MODULE: Grounding Checker

Project:
Authentic AI Search

Engine:
VRA Intelligence

Purpose:
Verify answer grounding.

Author:
Abhinav

Version:
1.0.0
=========================================================
"""

from typing import Dict, Any, List


class GroundingChecker:

    def evaluate(
        self,
        evidence_records: List[Dict[str, Any]]
    ) -> Dict[str, Any]:

        verified_count = sum(

            1

            for record in evidence_records

            if record.get(
                "retrieval_status"
            ) == "success"
        )

        grounded = verified_count > 0

        return {

            "grounded": grounded,

            "verified_source_count":
            verified_count
        }