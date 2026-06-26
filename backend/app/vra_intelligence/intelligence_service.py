"""
=========================================================
MODULE: Intelligence Service

Project:
Authentic AI Search

Engine:
VRA Intelligence

Purpose:
Public service interface for VRA Intelligence.

Author:
Abhinav

Version:
1.0.0
=========================================================
"""

from typing import Any
from typing import Dict

from backend.app.vra_intelligence.intelligence_orchestrator import (
    IntelligenceOrchestrator
)

from backend.app.vra_intelligence.final_response_builder import (
    FinalResponseBuilder
)


class IntelligenceService:
    """
    Service wrapper for VRA Intelligence.

    This is the clean interface that will later be called
    from chat.py or pipeline.py.
    """

    def __init__(self) -> None:
        self.orchestrator = IntelligenceOrchestrator()
        self.response_builder = FinalResponseBuilder()

    def process(
        self,
        query: str,
        vra_result: Any | None = None,
        extra_context: Dict[str, Any] | None = None
    ) -> Dict[str, Any]:
        """
        Process query through VRA Intelligence.
        """

        orchestration_result = self.orchestrator.run(
            query=query,
            vra_result=vra_result,
            extra_context=extra_context
        )

        final_response = self.response_builder.build(
            orchestration_result
        )

        return final_response