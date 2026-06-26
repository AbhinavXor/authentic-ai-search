"""
=========================================================
MODULE: Memory Manager
=========================================================
"""

from typing import Any, Dict

from backend.app.vra_intelligence.memory.conversation_memory import (
    ConversationMemory
)

from backend.app.vra_intelligence.memory.user_preference_memory import (
    UserPreferenceMemory
)

from backend.app.vra_intelligence.memory.project_memory import (
    ProjectMemory
)

from backend.app.vra_intelligence.memory.research_memory import (
    ResearchMemory
)


class MemoryManager:

    def __init__(self) -> None:

        self.conversation_memory = ConversationMemory()
        self.user_preference_memory = UserPreferenceMemory()
        self.project_memory = ProjectMemory()
        self.research_memory = ResearchMemory()

    def build_memory_context(
        self
    ) -> Dict[str, Any]:

        return {
            "recent_messages":
            self.conversation_memory.get_recent(),

            "preferences":
            self.user_preference_memory.get_all(),

            "recent_research":
            self.research_memory.get_recent()
        }