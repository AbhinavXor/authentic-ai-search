"""
=========================================================
MODULE: VIAA Allocation Decision Engine

Project:
Authentic AI Search

Engine:
VRA Intelligence Allocation Algorithm (VIAA)

Purpose:
Decide final worker allocation strategy.

Author:
Abhinav

Version:
1.0.0
=========================================================
"""

from typing import Any, Dict, List


class AllocationDecisionEngine:
    """
    Decide how work should be allocated.
    """

    def __init__(self) -> None:
        pass

    def decide(
        self,
        intelligence_plan: Dict[str, Any],
        routed_workers: List[str]
    ) -> Dict[str, Any]:
        """
        Decide allocation mode and priority.
        """

        complexity_result = intelligence_plan.get(
            "complexity_result",
            {}
        )

        task_result = intelligence_plan.get(
            "task_result",
            {}
        )

        output_plan = intelligence_plan.get(
            "output_plan",
            {}
        )

        complexity_level = complexity_result.get(
            "complexity_level",
            "simple"
        )

        primary_task = task_result.get(
            "primary_task",
            "general_chat"
        )

        blocks = output_plan.get(
            "blocks",
            []
        )

        allocation_mode = "single_worker"

        if complexity_level in {
            "complex",
            "expert"
        }:
            allocation_mode = "multi_worker"

        if primary_task in {
            "research",
            "pdf",
            "ppt",
            "docx"
        }:
            allocation_mode = "multi_worker"

        if any(
            block in blocks
            for block in [
                "chart",
                "pdf_preview",
                "ppt_preview",
                "document_preview"
            ]
        ):
            allocation_mode = "artifact_worker_required"

        priority_workers = []

        for worker in routed_workers:
            if worker not in priority_workers:
                priority_workers.append(worker)

        if allocation_mode != "single_worker":
            if "verification_worker" not in priority_workers:
                priority_workers.append("verification_worker")

        if primary_task == "research":
            if "research_worker" not in priority_workers:
                priority_workers.insert(0, "research_worker")

        if primary_task == "math_science":
            if "reasoning_worker" not in priority_workers:
                priority_workers.insert(0, "reasoning_worker")

        return {
            "allocation_mode": allocation_mode,
            "primary_task": primary_task,
            "complexity_level": complexity_level,
            "priority_workers": priority_workers,
            "requires_verification": True,
            "requires_vra_grounding": True
        }