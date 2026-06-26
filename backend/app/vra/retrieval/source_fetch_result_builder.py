"""
=========================================================
MODULE: Source Fetch Result Builder

Project:
Authentic AI Search

Engine:
VRA Search Engine

Purpose:
Standardize fetch outputs from all retrieval modules.

Author:
Abhinav

Version:
1.0.0
=========================================================
"""

from typing import Any, Dict


class SourceFetchResultBuilder:
    """
    Creates standardized fetch results.

    All fetchers should eventually return
    the same structure through this builder.
    """

    def __init__(self) -> None:
        pass

    def build_success(
        self,
        source_url: str,
        source_type: str,
        page_title: str = "",
        page_description: str = "",
        page_text: str = "",
        raw_html: str = "",
        metadata: Dict[str, Any] | None = None,
        additional_data: Dict[str, Any] | None = None
    ) -> Dict[str, Any]:
        """
        Build successful fetch result.
        """

        return {
            "status": "success",
            "retrieval_status": "success",
            "source_url": source_url,
            "source_type": source_type,
            "page_title": page_title,
            "page_description": page_description,
            "page_text": page_text,
            "raw_html": raw_html,
            "metadata": metadata or {},
            "additional_data": additional_data or {},
            "error": None
        }

    def build_failure(
        self,
        source_url: str,
        source_type: str,
        error: str
    ) -> Dict[str, Any]:
        """
        Build failed fetch result.
        """

        return {
            "status": "failed",
            "retrieval_status": "failed",
            "source_url": source_url,
            "source_type": source_type,
            "page_title": "",
            "page_description": "",
            "page_text": "",
            "raw_html": "",
            "metadata": {},
            "additional_data": {},
            "error": error
        }