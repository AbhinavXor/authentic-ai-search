"""
=========================================================
MODULE: VIAA Execution Engine

Project:
Authentic AI Search

Engine:
VRA Intelligence

Purpose:
Execute VIAA worker plans and merge worker outputs.

Author:
Abhinav

Version:
1.0.0
=========================================================
"""

from typing import Any
from typing import Dict
from typing import List

from backend.app.vra_intelligence.execution.worker_factory import (
    WorkerFactory
)
from backend.app.vra_intelligence.execution.worker_executor import (
    WorkerExecutor
)
from backend.app.vra_intelligence.execution.worker_result_merger import (
    WorkerResultMerger
)
from backend.app.vra_intelligence.execution.execution_monitor import (
    ExecutionMonitor
)


class VIAAExecutionEngine:
    """
    Executes VIAA plans using worker system.
    """

    def __init__(self) -> None:

        self.worker_factory = WorkerFactory()
        self.worker_executor = WorkerExecutor()
        self.result_merger = WorkerResultMerger()
        self.execution_monitor = ExecutionMonitor()

    def _extract_worker_names(
        self,
        execution_plan: Dict[str, Any]
    ) -> List[str]:
        """
        Extract ordered worker names from execution plan.
        """

        plan = execution_plan.get(
            "execution_plan",
            {}
        )

        steps = plan.get(
            "execution_steps",
            []
        )

        worker_names = []

        for step in steps:

            worker_name = step.get(
                "worker"
            )

            if worker_name:
                worker_names.append(
                    worker_name
                )

        return worker_names

    def execute(
        self,
        execution_plan: Dict[str, Any],
        context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Execute VIAA plan.
        """

        worker_names = self._extract_worker_names(
            execution_plan
        )

        workers = self.worker_factory.create_many(
            worker_names
        )

        execution_result = self.worker_executor.execute_plan(
            workers=workers,
            context=context
        )

        merged_result = self.result_merger.merge(
            execution_result.get(
                "worker_results",
                []
            )
        )

        metrics = self.execution_monitor.build_metrics(
            execution_result
        )

        return {
            "status": "completed",
            "worker_names": worker_names,
            "execution_result": execution_result,
            "merged_result": merged_result,
            "metrics": metrics
        }