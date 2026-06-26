"""
=========================================================
MODULE: Multimodal Router

Project:
Authentic AI Search

Engine:
VRA Intelligence

Purpose:
Route multimodal requests.

Author:
Abhinav

Version:
1.0.0
=========================================================
"""

from typing import Any, Dict

from backend.app.vra_intelligence.multimodal.image_request_detector import (
    ImageRequestDetector
)

from backend.app.vra_intelligence.multimodal.document_request_detector import (
    DocumentRequestDetector
)

from backend.app.vra_intelligence.multimodal.vision_plan_builder import (
    VisionPlanBuilder
)

from backend.app.vra_intelligence.multimodal.multimodal_context_builder import (
    MultimodalContextBuilder
)


class MultimodalRouter:
    """
    Main multimodal planning router.
    """

    def __init__(self) -> None:
        self.image_detector = ImageRequestDetector()
        self.document_detector = DocumentRequestDetector()
        self.vision_plan_builder = VisionPlanBuilder()
        self.context_builder = MultimodalContextBuilder()

    def route(
        self,
        query: str,
        file_path: str | None = None,
        file_type: str | None = None,
        metadata: Dict[str, Any] | None = None
    ) -> Dict[str, Any]:
        """
        Route multimodal request.
        """

        has_uploaded_file = file_path is not None

        has_uploaded_image = (
            has_uploaded_file
            and file_type in {
                "image/png",
                "image/jpeg",
                "image/jpg",
                "image/webp",
                "image/heic"
            }
        )

        image_result = self.image_detector.detect(
            query=query,
            has_uploaded_image=has_uploaded_image
        )

        document_result = self.document_detector.detect(
            query=query,
            has_uploaded_file=has_uploaded_file
        )

        vision_plan = self.vision_plan_builder.build(
            image_result=image_result,
            document_result=document_result
        )

        context = self.context_builder.build(
            query=query,
            file_path=file_path,
            file_type=file_type,
            metadata=metadata
        )

        return {
            "image_result": image_result,
            "document_result": document_result,
            "vision_plan": vision_plan,
            "multimodal_context": context
        }