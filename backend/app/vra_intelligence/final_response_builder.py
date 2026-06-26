"""
=========================================================
MODULE: Final Response Builder

Project:
Authentic AI Search

Engine:
VRA Intelligence

Purpose:
Build clean API/frontend-friendly response from
VRA Intelligence execution output.

Author:
Abhinav

Version:
1.0.0
=========================================================
"""

from typing import Any
from typing import Dict


class FinalResponseBuilder:
    """
    Builds final structured response.
    """

    def build(
        self,
        orchestration_result: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Build final response.
        """

        execution_result = orchestration_result.get(
            "execution_result",
            {}
        )

        merged_result = execution_result.get(
            "merged_result",
            {}
        )

        intelligence_plan = orchestration_result.get(
            "intelligence_plan",
            {}
        )

        viaa_plan = orchestration_result.get(
            "viaa_plan",
            {}
        )

        return {
            "status": orchestration_result.get(
                "status",
                "unknown"
            ),
            "query": orchestration_result.get(
                "query",
                ""
            ),
            "answer": merged_result.get(
                "answer",
                ""
            ),
            "sources": merged_result.get(
                "sources",
                []
            ),
            "citations": merged_result.get(
                "citations",
                []
            ),
            "evidence_records": merged_result.get(
                "evidence_records",
                []
            ),
            "verification_result": merged_result.get(
                "verification_result",
                {}
            ),
            "worker_results": merged_result.get(
                "worker_results",
                []
            ),
            "metrics": execution_result.get(
                "metrics",
                {}
            ),
            "intelligence_plan": intelligence_plan,
            "viaa_plan": viaa_plan,
            "output_plan": intelligence_plan.get(
                "output_plan",
                {}
            )
        }