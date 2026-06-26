"""
=========================================================
MODULE: Worker Executor

Project:
Authentic AI Search

Engine:
VRA Intelligence

Purpose:
Execute workers.

Author:
Abhinav

Version:
2.0.0
=========================================================
"""

from typing import Dict
from typing import Any
from typing import List


class WorkerExecutor:

    def execute_worker(
        self,
        worker,
        context: Dict[str, Any]
    ) -> Dict[str, Any]:

        try:

            result = worker.execute(
                context
            )

            return {
                "status": "success",
                "result": result
            }

        except Exception as error:

            return {
                "status": "failed",
                "error": str(error)
            }

    def execute_plan(
        self,
        workers: List[Any],
        context: Dict[str, Any]
    ) -> Dict[str, Any]:

        worker_results = []

        for worker in workers:

            result = (
                self.execute_worker(
                    worker,
                    context
                )
            )

            worker_results.append(
                result
            )

        return {

            "status":
            "completed",

            "worker_count":
            len(worker_results),

            "worker_results":
            worker_results
        }