"""
=========================================================
MODULE: Execution Monitor

Project:
Authentic AI Search

Engine:
VRA Intelligence

Purpose:
Build execution metrics for VIAA worker runs.

Author:
Abhinav

Version:
2.0.0
=========================================================
"""

from typing import Any
from typing import Dict
from typing import List


class ExecutionMonitor:
    """
    Tracks execution result metrics.
    """

    def build_metrics(
        self,
        execution_result: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Build execution metrics.
        """

        worker_results: List[Dict[str, Any]] = (
            execution_result.get(
                "worker_results",
                []
            )
        )

        success_count = 0
        failed_count = 0

        failed_workers = []

        for item in worker_results:
            if item.get("status") == "success":
                success_count += 1
            else:
                failed_count += 1
                failed_workers.append(
                    item.get("worker")
                    or item.get("result", {}).get("worker")
                    or "unknown"
                )

        total_count = len(worker_results)

        success_rate = 0.0

        if total_count > 0:
            success_rate = round(
                success_count / total_count,
                2
            )

        return {
            "execution_status": execution_result.get(
                "status",
                "unknown"
            ),
            "total_workers": total_count,
            "successful_workers": success_count,
            "failed_workers": failed_count,
            "failed_worker_names": failed_workers,
            "success_rate": success_rate
        }