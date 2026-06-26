"""
=========================================================
MODULE: Agent Manager

Project:
Authentic AI Search

Engine:
VRA Intelligence

Purpose:
Main manager for agentic workflows.

Author:
Abhinav

Version:
1.0.0
=========================================================
"""

from typing import Any, Dict

from backend.app.vra_intelligence.agentic.task_decomposer import (
    TaskDecomposer
)

from backend.app.vra_intelligence.agentic.objective_planner import (
    ObjectivePlanner
)

from backend.app.vra_intelligence.agentic.execution_coordinator import (
    ExecutionCoordinator
)


class AgentManager:
    """
    Main agentic workflow manager.
    """

    def __init__(self) -> None:

        self.task_decomposer = TaskDecomposer()
        self.objective_planner = ObjectivePlanner()
        self.execution_coordinator = ExecutionCoordinator()

    def build_agent_plan(
        self,
        query: str
    ) -> Dict[str, Any]:

        objective_plan = self.objective_planner.plan(
            query
        )

        decomposition = self.task_decomposer.decompose(
            query
        )

        execution_plan = self.execution_coordinator.coordinate(
            objective_plan=objective_plan,
            decomposition=decomposition
        )

        return {
            "agentic_mode": decomposition.get("step_count", 0) > 1,
            "objective_plan": objective_plan,
            "decomposition": decomposition,
            "execution_plan": execution_plan
        }