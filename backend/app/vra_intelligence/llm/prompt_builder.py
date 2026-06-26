"""
=========================================================
MODULE: Prompt Builder
=========================================================
"""

from typing import Dict


class PromptBuilder:

    def build(
        self,
        query: str,
        task_type: str
    ) -> Dict:

        system_prompt = (
            "You are VRA Intelligence."
        )

        return {

            "system_prompt":
            system_prompt,

            "user_prompt":
            query,

            "task_type":
            task_type
        }