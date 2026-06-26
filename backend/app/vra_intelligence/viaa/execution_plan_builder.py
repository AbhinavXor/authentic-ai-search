"""
=========================================================
MODULE: VIAA Execution Plan Builder

Project:
Authentic AI Search

Engine:
VRA Intelligence Allocation Algorithm (VIAA)

Purpose:
Build ordered execution plan from allocation decision.

Author:
Abhinav

Version:
1.0.0
=========================================================
"""

from typing import Any, Dict, List


class ExecutionPlanBuilder:
    """
    Builds executable worker plan for VIAA.
    """

    def __init__(self) -> None:
        pass

    def build(
        self,
        allocation_decision: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Build execution plan.
        """

        priority_workers = allocation_decision.get(
            "priority_workers",
            []
        )

        allocation_mode = allocation_decision.get(
            "allocation_mode",
            "single_worker"
        )

        execution_steps: List[Dict[str, Any]] = []

        for index, worker in enumerate(
            priority_workers,
            start=1
        ):
            execution_steps.append(
                {
                    "step": index,
                    "worker": worker,
                    "required": True,
                    "status": "pending"
                }
            )

        if allocation_decision.get(
            "requires_verification",
            True
        ):
            if not any(
                step.get("worker") == "verification_worker"
                for step in execution_steps
            ):
                execution_steps.append(
                    {
                        "step": len(execution_steps) + 1,
                        "worker": "verification_worker",
                        "required": True,
                        "status": "pending"
                    }
                )

        return {
            "allocation_mode": allocation_mode,
            "execution_steps": execution_steps,
            "requires_vra_grounding": allocation_decision.get(
                "requires_vra_grounding",
                True
            ),
            "plan_status": "created"
        }