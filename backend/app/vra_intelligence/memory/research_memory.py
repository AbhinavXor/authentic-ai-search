"""
=========================================================
MODULE: Research Memory
=========================================================
"""

from typing import Any, Dict, List


class ResearchMemory:

    def __init__(self) -> None:
        self.research_items: List[Dict[str, Any]] = []

    def add_research_item(
        self,
        item: Dict[str, Any]
    ) -> None:

        self.research_items.append(item)

    def get_recent(
        self,
        limit: int = 10
    ) -> List[Dict[str, Any]]:

        return self.research_items[-limit:]