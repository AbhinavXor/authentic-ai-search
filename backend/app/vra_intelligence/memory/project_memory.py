"""
=========================================================
MODULE: Project Memory
=========================================================
"""

from typing import Any, Dict, List


class ProjectMemory:

    def __init__(self) -> None:
        self.projects: Dict[str, List[Dict[str, Any]]] = {}

    def add_project_item(
        self,
        project_id: str,
        item: Dict[str, Any]
    ) -> None:

        if project_id not in self.projects:
            self.projects[project_id] = []

        self.projects[project_id].append(item)

    def get_project_items(
        self,
        project_id: str
    ) -> List[Dict[str, Any]]:

        return self.projects.get(
            project_id,
            []
        )