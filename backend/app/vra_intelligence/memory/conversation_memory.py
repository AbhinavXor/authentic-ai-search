"""
=========================================================
MODULE: Conversation Memory
=========================================================
"""

from typing import Any, Dict, List


class ConversationMemory:

    def __init__(self) -> None:
        self.messages: List[Dict[str, Any]] = []

    def add_message(
        self,
        role: str,
        content: str,
        metadata: Dict[str, Any] | None = None
    ) -> None:

        self.messages.append(
            {
                "role": role,
                "content": content,
                "metadata": metadata or {}
            }
        )

    def get_recent(
        self,
        limit: int = 10
    ) -> List[Dict[str, Any]]:

        return self.messages[-limit:]