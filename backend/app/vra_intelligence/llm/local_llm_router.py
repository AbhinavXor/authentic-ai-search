"""
=========================================================
MODULE: Local LLM Router
=========================================================
"""

from typing import Dict
from typing import Any

from backend.app.vra_intelligence.llm.model_selector import (
    ModelSelector
)

from backend.app.vra_intelligence.llm.prompt_builder import (
    PromptBuilder
)

from backend.app.vra_intelligence.llm.providers.ollama_provider import (
    OllamaProvider
)


class LocalLLMRouter:

    def __init__(self) -> None:

        self.selector = ModelSelector()

        self.prompt_builder = (
            PromptBuilder()
        )

        self.ollama = (
            OllamaProvider()
        )

    def generate(
        self,
        query: str,
        task_type: str = "chat"
    ) -> Dict[str, Any]:

        selected_model = (
            self.selector.select(
                task_type
            )
        )

        model_name = (
            selected_model[
                "model_name"
            ]
        )

        prompt_data = (
            self.prompt_builder.build(
                query=query,
                task_type=task_type
            )
        )

        return self.ollama.generate(
            model_name=model_name,
            prompt=prompt_data[
                "user_prompt"
            ],
            system_prompt=prompt_data[
                "system_prompt"
            ]
        )