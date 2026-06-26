"""
=========================================================
MODULE: Execution Context Builder

Project:
Authentic AI Search

Engine:
VRA Intelligence

Purpose:
Build clean execution context for VIAA workers.

Author:
Abhinav

Version:
2.0.0
=========================================================
"""

from dataclasses import asdict, is_dataclass
from typing import Any, Dict


class ExecutionContextBuilder:
    """
    Builds execution context for workers.

    This keeps all workers using one common structure.
    """

    def _to_dict(
        self,
        value: Any
    ) -> Any:
        """
        Convert dataclass objects to dictionaries.
        """

        if is_dataclass(value):
            return asdict(value)

        return value

    def build(
        self,
        query: str,
        intelligence_plan: Dict[str, Any],
        vra_result: Any | None = None,
        extra_context: Dict[str, Any] | None = None
    ) -> Dict[str, Any]:
        """
        Build worker execution context.
        """

        context: Dict[str, Any] = {
            "query": query,
            "intelligence_plan": intelligence_plan,
            "vra_result": self._to_dict(vra_result),
            "extra_context": extra_context or {}
        }

        if vra_result:
            context.update(
                {
                    "answer": getattr(
                        vra_result,
                        "answer",
                        ""
                    ),
                    "trust_score": getattr(
                        vra_result,
                        "trust_score",
                        0
                    ),
                    "confidence_score": getattr(
                        vra_result,
                        "confidence_score",
                        0
                    ),
                    "verification_status": getattr(
                        vra_result,
                        "verification_status",
                        "unknown"
                    ),
                    "verification_badge": getattr(
                        vra_result,
                        "verification_badge",
                        ""
                    ),
                    "sources": getattr(
                        vra_result,
                        "sources",
                        []
                    ),
                    "evidence_records": getattr(
                        vra_result,
                        "evidence_records",
                        []
                    ),
                    "evidence_summary": getattr(
                        vra_result,
                        "evidence_summary",
                        []
                    ),
                    "citations": getattr(
                        vra_result,
                        "citations",
                        []
                    ),
                    "warning_message": getattr(
                        vra_result,
                        "warning_message",
                        None
                    )
                }
            )

        return context