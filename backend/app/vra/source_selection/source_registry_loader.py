"""
=========================================================
MODULE: Source Registry Loader

Project:
Authentic AI Search

Engine:
Verified Resource Algorithm (VRA)

Purpose:
Load trusted source registry JSON files from the
source_registry directory.

Why this module exists:
VRA should not randomly trust websites.
It should first read approved sources from a
controlled registry.

Author:
Abhinav

Version:
0.1.0
=========================================================
"""

import json
from pathlib import Path
from typing import Any, Dict, List


class SourceRegistryLoader:
    """
    Loads verified/trusted source registries from JSON files.

    Current Responsibility:
    - Read JSON files from source_registry/
    - Return all sources as Python dictionaries

    Future Responsibility:
    - Validate JSON schema
    - Filter by country
    - Filter by source category
    - Sync registry with database
    - Track registry version changes
    """

    def __init__(self, registry_root: str = "source_registry") -> None:
        """
        Initialize registry loader.

        Args:
            registry_root:
                Root folder where all source registry JSON files are stored.
        """

        self.registry_root = Path(registry_root)

    def load_registry_file(self, file_path: Path) -> Dict[str, Any]:
        """
        Load a single JSON registry file.

        Args:
            file_path:
                Full path of the JSON file.

        Returns:
            Parsed JSON data as dictionary.
        """

        with file_path.open("r", encoding="utf-8") as file:
            return json.load(file)

    def load_all_sources(self) -> List[Dict[str, Any]]:
        """
        Load all source entries from all JSON registry files.

        Returns:
            List of source dictionaries.
        """

        all_sources: List[Dict[str, Any]] = []

        json_files = sorted(self.registry_root.rglob("*.json"))

        for json_file in json_files:
            registry_data = self.load_registry_file(json_file)

            registry_sources = registry_data.get("sources", [])

            for source in registry_sources:
                source["registry_file"] = str(json_file)
                source["registry_category"] = registry_data.get("category")
                all_sources.append(source)

        return all_sources
