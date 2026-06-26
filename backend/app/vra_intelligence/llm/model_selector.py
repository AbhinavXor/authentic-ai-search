"""
=========================================================
MODULE: Model Selector
=========================================================
"""

from typing import Dict

from backend.app.vra_intelligence.llm.model_capabilities import (
    MODEL_CAPABILITIES
)


class ModelSelector:

    def select(
        self,
        task_type: str
    ) -> Dict:

        for model_name, config in (
            MODEL_CAPABILITIES.items()
        ):

            if task_type in config.get(
                "strengths",
                []
            ):

                return {
                    "model_name":
                    model_name,

                    "model_config":
                    config
                }

        return {

            "model_name":
            "qwen3",

            "model_config":
            MODEL_CAPABILITIES["qwen3"]
        }