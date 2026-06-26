"""
=========================================================
MODULE: Image Generation Worker

Project:
Authentic AI Search

Engine:
VRA Intelligence

Purpose:
Plan image/logo/poster/banner generation workflows.

Author:
Abhinav

Version:
2.0.0
=========================================================
"""

from typing import Any, Dict

from backend.app.vra_intelligence.workers.base_worker import (
    BaseWorker
)


class ImageGenerationWorker(BaseWorker):
    """
    Image generation worker.

    MVP:
    - Detects image generation request.
    - Builds image generation plan.
    - Future: connect OpenAI Image, Stability, Ideogram, or local FLUX/SDXL.
    """

    @property
    def worker_name(self) -> str:
        return "image_generation_worker"

    def _select_image_type(
        self,
        query: str
    ) -> str:
        query_lower = query.lower()

        if "logo" in query_lower:
            return "logo"

        if "poster" in query_lower:
            return "poster"

        if "banner" in query_lower:
            return "banner"

        if "illustration" in query_lower:
            return "illustration"

        if "ui" in query_lower or "mockup" in query_lower:
            return "ui_mockup"

        return "general_image"

    def _select_style(
        self,
        query: str
    ) -> str:
        query_lower = query.lower()

        if "professional" in query_lower:
            return "professional"

        if "minimal" in query_lower:
            return "minimal"

        if "realistic" in query_lower:
            return "realistic"

        if "cartoon" in query_lower:
            return "cartoon"

        if "3d" in query_lower:
            return "3d"

        if "colorful" in query_lower:
            return "colorful"

        return "standard"

    def execute(
        self,
        context: Dict[str, Any]
    ) -> Dict[str, Any]:

        query = context.get("query", "")

        image_type = self._select_image_type(
            query
        )

        style = self._select_style(
            query
        )

        return {
            "worker": self.worker_name,
            "status": "completed",
            "query": query,
            "answer": (
                "An image generation workflow can be used for this request. "
                "The image generation worker has prepared a generation plan."
            ),
            "image_generation_required": True,
            "image_type": image_type,
            "style": style,
            "image_generation_plan": {
                "prompt": query,
                "image_type": image_type,
                "style": style,
                "primary_provider": "openai_image",
                "fallback_providers": [
                    "stability_ai",
                    "ideogram",
                    "replicate",
                    "fal_ai"
                ],
                "local_future_option": [
                    "flux",
                    "stable_diffusion_xl"
                ]
            }
        }