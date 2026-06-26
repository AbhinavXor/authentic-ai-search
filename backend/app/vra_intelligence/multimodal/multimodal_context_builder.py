"""
=========================================================
MODULE: Multimodal Context Builder

Project:
Authentic AI Search

Engine:
VRA Intelligence

Purpose:
Build context object for multimodal execution.

Author:
Abhinav

Version:
1.0.0
=========================================================
"""

from typing import Any, Dict


class MultimodalContextBuilder:
    """
    Build multimodal context.
    """

    def build(
        self,
        query: str,
        file_path: str | None = None,
        file_type: str | None = None,
        metadata: Dict[str, Any] | None = None
    ) -> Dict[str, Any]:
        """
        Build multimodal context.
        """

        return {
            "query": query,
            "file_path": file_path,
            "file_type": file_type,
            "metadata": metadata or {}
        }