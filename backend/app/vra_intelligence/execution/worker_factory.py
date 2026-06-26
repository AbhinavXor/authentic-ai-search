"""
=========================================================
MODULE: Worker Factory

Project:
Authentic AI Search

Engine:
VRA Intelligence

Purpose:
Create worker instances from worker names.

Author:
Abhinav

Version:
1.0.0
=========================================================
"""

from typing import Any

from backend.app.vra_intelligence.workers.search_worker import (
    SearchWorker
)
from backend.app.vra_intelligence.workers.research_worker import (
    ResearchWorker
)
from backend.app.vra_intelligence.workers.reasoning_worker import (
    ReasoningWorker
)
from backend.app.vra_intelligence.workers.verification_worker import (
    VerificationWorker
)
from backend.app.vra_intelligence.workers.chart_worker import (
    ChartWorker
)
from backend.app.vra_intelligence.workers.pdf_worker import (
    PDFWorker
)
from backend.app.vra_intelligence.workers.ppt_worker import (
    PPTWorker
)
from backend.app.vra_intelligence.workers.document_worker import (
    DocumentWorker
)
from backend.app.vra_intelligence.workers.vision_worker import (
    VisionWorker
)
from backend.app.vra_intelligence.workers.image_generation_worker import (
    ImageGenerationWorker
)
from backend.app.vra_intelligence.workers.code_worker import (
    CodeWorker
)
from backend.app.vra_intelligence.workers.emotional_worker import (
    EmotionalWorker
)
from backend.app.vra_intelligence.workers.general_worker import (
    GeneralWorker
)


class WorkerFactory:
    """
    Creates VIAA worker instances.
    """

    def __init__(self) -> None:
        self.worker_classes = {
            "search_worker": SearchWorker,
            "research_worker": ResearchWorker,
            "reasoning_worker": ReasoningWorker,
            "verification_worker": VerificationWorker,
            "chart_worker": ChartWorker,
            "pdf_worker": PDFWorker,
            "ppt_worker": PPTWorker,
            "document_worker": DocumentWorker,
            "vision_worker": VisionWorker,
            "image_generation_worker": ImageGenerationWorker,
            "code_worker": CodeWorker,
            "emotional_worker": EmotionalWorker,
            "general_worker": GeneralWorker
        }

    def create(
        self,
        worker_name: str
    ) -> Any | None:
        """
        Create one worker instance.
        """

        worker_class = self.worker_classes.get(
            worker_name
        )

        if not worker_class:
            return None

        return worker_class()

    def create_many(
        self,
        worker_names: list[str]
    ) -> list[Any]:
        """
        Create multiple worker instances.
        """

        workers = []

        for worker_name in worker_names:
            worker = self.create(worker_name)

            if worker:
                workers.append(worker)

        return workers