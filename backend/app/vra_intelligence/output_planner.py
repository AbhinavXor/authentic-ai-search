"""
=========================================================
MODULE: Output Planner

Project:
Authentic AI Search

Engine:
VRA Intelligence

Purpose:
Plan final response layout and output blocks.

Author:
Abhinav

Version:
1.0.0
=========================================================
"""

from typing import Any, Dict, List


class OutputPlanner:
    """
    Plans output structure for frontend rendering.

    Future:
    - Artifact canvas support
    - Chart blocks
    - PDF previews
    - Live editable documents
    """

    def __init__(self) -> None:
        pass

    def plan(
        self,
        task_result: Dict[str, Any],
        complexity_result: Dict[str, Any],
        worker_result: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Create output plan.
        """

        primary_task = task_result.get(
            "primary_task",
            "general_chat"
        )

        complexity_level = complexity_result.get(
            "complexity_level",
            "simple"
        )

        blocks: List[str] = [
            "answer"
        ]

        if primary_task in {
            "search",
            "research",
            "general_chat"
        }:
            blocks.extend(
                [
                    "source_cards",
                    "verification_badge"
                ]
            )

        if primary_task == "research":
            blocks.extend(
                [
                    "key_points",
                    "citations",
                    "evidence_summary"
                ]
            )

        if primary_task == "chart":
            blocks.extend(
                [
                    "chart",
                    "chart_explanation"
                ]
            )

        if primary_task == "pdf":
            blocks.extend(
                [
                    "pdf_preview",
                    "download_button"
                ]
            )

        if primary_task == "ppt":
            blocks.extend(
                [
                    "ppt_preview",
                    "download_button"
                ]
            )

        if primary_task == "docx":
            blocks.extend(
                [
                    "document_preview",
                    "download_button"
                ]
            )

        if primary_task == "coding":
            blocks.extend(
                [
                    "code_block",
                    "explanation"
                ]
            )

        if primary_task == "math_science":
            blocks.extend(
                [
                    "step_by_step",
                    "formula_block"
                ]
            )

        if primary_task == "image_analysis":
            blocks.extend(
                [
                    "image_preview",
                    "ocr_text",
                    "image_findings"
                ]
            )

        if primary_task == "image_generation":
            blocks.extend(
                [
                    "generated_image",
                    "prompt_controls"
                ]
            )

        if complexity_level in {
            "complex",
            "expert"
        }:
            blocks.append(
                "structured_sections"
            )

        blocks.append(
            "verification_details_toggle"
        )

        return {
            "output_mode": primary_task,
            "complexity_level": complexity_level,
            "blocks": blocks,
            "selected_worker": worker_result.get(
                "selected_worker"
            ),
            "execution_mode": worker_result.get(
                "execution_mode"
            )
        }