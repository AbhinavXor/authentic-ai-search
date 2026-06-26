"""
=========================================================
MODULE: Intelligence Orchestrator

Project:
Authentic AI Search

Engine:
VRA Intelligence

Purpose:
Orchestrate query analysis, VIAA planning, and worker execution.

Author:
Abhinav

Version:
1.0.0
=========================================================
"""

from typing import Any
from typing import Dict

from backend.app.vra_intelligence.intelligence_engine import (
    IntelligenceEngine
)

from backend.app.vra_intelligence.viaa.viaa_engine import (
    VIAAEngine
)

from backend.app.vra_intelligence.execution.execution_context_builder import (
    ExecutionContextBuilder
)

from backend.app.vra_intelligence.execution.viaa_execution_engine import (
    VIAAExecutionEngine
)


class IntelligenceOrchestrator:
    """
    Top-level VRA Intelligence orchestrator.

    Flow:
    Query
    → Intelligence Plan
    → VIAA Execution Plan
    → Worker Execution
    → Merged Result
    """

    def __init__(self) -> None:

        self.intelligence_engine = IntelligenceEngine()
        self.viaa_engine = VIAAEngine()
        self.context_builder = ExecutionContextBuilder()
        self.execution_engine = VIAAExecutionEngine()

    def run(
        self,
        query: str,
        vra_result: Any | None = None,
        extra_context: Dict[str, Any] | None = None
    ) -> Dict[str, Any]:
        """
        Run complete intelligence orchestration.
        """

        intelligence_plan = self.intelligence_engine.analyze_query(
            query=query
        )

        viaa_plan = self.viaa_engine.create_execution_plan(
            intelligence_plan=intelligence_plan
        )

        execution_context = self.context_builder.build(
            query=query,
            intelligence_plan=intelligence_plan,
            vra_result=vra_result,
            extra_context=extra_context
        )

        execution_result = self.execution_engine.execute(
            execution_plan=viaa_plan,
            context=execution_context
        )

        return {
            "status": "completed",
            "query": query,
            "intelligence_plan": intelligence_plan,
            "viaa_plan": viaa_plan,
            "execution_context": execution_context,
            "execution_result": execution_result
        }