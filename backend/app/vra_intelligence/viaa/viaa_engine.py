"""
=========================================================
MODULE: VIAA Engine

Project:
Authentic AI Search

Engine:
VRA Intelligence Allocation Algorithm (VIAA)

Purpose:
Main orchestration engine for worker allocation.

Author:
Abhinav

Version:
1.0.0
=========================================================
"""

from typing import Any, Dict

from backend.app.vra_intelligence.viaa.task_router import (
    TaskRouter
)

from backend.app.vra_intelligence.viaa.worker_registry import (
    WorkerRegistry
)

from backend.app.vra_intelligence.viaa.allocation_decision_engine import (
    AllocationDecisionEngine
)

from backend.app.vra_intelligence.viaa.execution_plan_builder import (
    ExecutionPlanBuilder
)


class VIAAEngine:
    """
    Main VIAA orchestrator.

    Future:
    - Multi-worker execution
    - Local LLM orchestration
    - API fallback orchestration
    - Cost optimization
    - Worker health monitoring
    """

    def __init__(self) -> None:

        self.task_router = TaskRouter()

        self.worker_registry = WorkerRegistry()

        self.allocation_engine = (
            AllocationDecisionEngine()
        )

        self.execution_plan_builder = (
            ExecutionPlanBuilder()
        )

    def create_execution_plan(
        self,
        intelligence_plan: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Build VIAA execution plan.
        """

        routing_result = (
            self.task_router.route(
                intelligence_plan
            )
        )

        routed_workers = (
            routing_result.get(
                "routed_workers",
                []
            )
        )

        available_workers = []

        for worker in routed_workers:

            if self.worker_registry.worker_exists(
                worker
            ):
                available_workers.append(
                    worker
                )

        allocation_decision = (
            self.allocation_engine.decide(
                intelligence_plan=
                intelligence_plan,

                routed_workers=
                available_workers
            )
        )

        execution_plan = (
            self.execution_plan_builder.build(
                allocation_decision
            )
        )

        return {
            "routing_result": routing_result,
            "allocation_decision": (
                allocation_decision
            ),
            "execution_plan": execution_plan
        }