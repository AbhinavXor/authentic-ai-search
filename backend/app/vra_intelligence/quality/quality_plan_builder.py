"""
=========================================================
MODULE: Quality Plan Builder

Project:
Authentic AI Search

Engine:
VRA Intelligence

Purpose:
Build final quality assessment.

Author:
Abhinav

Version:
1.0.0
=========================================================
"""

from typing import Dict, Any, List

from backend.app.vra_intelligence.quality.output_quality_checker import (
    OutputQualityChecker
)

from backend.app.vra_intelligence.quality.completeness_checker import (
    CompletenessChecker
)

from backend.app.vra_intelligence.quality.grounding_checker import (
    GroundingChecker
)


class QualityPlanBuilder:

    def __init__(
        self
    ) -> None:

        self.output_quality_checker = (
            OutputQualityChecker()
        )

        self.completeness_checker = (
            CompletenessChecker()
        )

        self.grounding_checker = (
            GroundingChecker()
        )

    def build(
        self,
        answer: str,
        evidence_records: List[Dict[str, Any]]
    ) -> Dict[str, Any]:

        quality_result = (
            self.output_quality_checker.evaluate(
                answer
            )
        )

        completeness_result = (
            self.completeness_checker.evaluate(
                answer
            )
        )

        grounding_result = (
            self.grounding_checker.evaluate(
                evidence_records
            )
        )

        return {

            "quality_result":
            quality_result,

            "completeness_result":
            completeness_result,

            "grounding_result":
            grounding_result
        }