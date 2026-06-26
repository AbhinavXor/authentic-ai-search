"""
=========================================================
MODULE: PDF Fetcher

Project:
Authentic AI Search

Engine:
VRA Search Engine

Purpose:
Download and extract text from PDF sources.

Author:
Abhinav

Version:
1.0.0
=========================================================
"""

from pathlib import Path
from typing import Any, Dict, Optional

import fitz
import requests
import urllib3


urllib3.disable_warnings(
    urllib3.exceptions.InsecureRequestWarning
)


class PDFFetcher:
    """
    Fetch and extract text from PDF files.

    This module is intentionally independent.
    It will be integrated into source_fetcher.py later.
    """

    def __init__(
        self,
        download_dir: str = "data/downloads/pdfs",
        timeout: int = 15
    ) -> None:
        self.download_dir = Path(download_dir)
        self.timeout = timeout

        self.download_dir.mkdir(
            parents=True,
            exist_ok=True
        )

    def _safe_filename(
        self,
        url: str
    ) -> str:
        """
        Generate safe local filename from URL.
        """

        filename = (
            url.replace("https://", "")
            .replace("http://", "")
            .replace("/", "_")
            .replace("?", "_")
            .replace("&", "_")
            .replace("=", "_")
        )

        if not filename.lower().endswith(".pdf"):
            filename = f"{filename}.pdf"

        return filename[:180]

    def download_pdf(
        self,
        url: str
    ) -> Dict[str, Optional[Any]]:
        """
        Download PDF from URL.
        """

        try:
            response = requests.get(
                url,
                timeout=self.timeout,
                verify=False,
                headers={
                    "User-Agent": (
                        "Mozilla/5.0 "
                        "AuthenticAISearch-VRA-PDF/1.0"
                    ),
                    "Accept": "application/pdf,*/*"
                }
            )

            if response.status_code != 200:
                return {
                    "status": "failed",
                    "status_code": response.status_code,
                    "file_path": None,
                    "error": (
                        f"HTTP status code {response.status_code}"
                    )
                }

            file_path = self.download_dir / self._safe_filename(
                url
            )

            with file_path.open("wb") as file:
                file.write(response.content)

            return {
                "status": "success",
                "status_code": response.status_code,
                "file_path": str(file_path),
                "error": None
            }

        except Exception as error:
            return {
                "status": "failed",
                "status_code": None,
                "file_path": None,
                "error": str(error)
            }

    def extract_text_from_file(
        self,
        file_path: str,
        max_chars: int = 8000
    ) -> Dict[str, Optional[Any]]:
        """
        Extract text from local PDF file.
        """

        try:
            document = fitz.open(file_path)

            page_texts = []

            for page_index in range(len(document)):
                page = document[page_index]
                text = page.get_text("text")

                if text:
                    page_texts.append(text)

                current_text = "\n".join(page_texts)

                if len(current_text) >= max_chars:
                    break

            document.close()

            extracted_text = "\n".join(page_texts).strip()

            if not extracted_text:
                return {
                    "status": "failed",
                    "text": None,
                    "page_count": len(page_texts),
                    "error": "No text extracted from PDF"
                }

            return {
                "status": "success",
                "text": extracted_text[:max_chars],
                "page_count": len(page_texts),
                "error": None
            }

        except Exception as error:
            return {
                "status": "failed",
                "text": None,
                "page_count": 0,
                "error": str(error)
            }

    def fetch_pdf_text(
        self,
        url: str,
        max_chars: int = 8000
    ) -> Dict[str, Optional[Any]]:
        """
        Download PDF and extract text.
        """

        download_result = self.download_pdf(
            url=url
        )

        if download_result.get("status") != "success":
            return {
                "status": "failed",
                "source_url": url,
                "file_path": None,
                "text": None,
                "page_count": 0,
                "error": download_result.get("error")
            }

        file_path = download_result.get("file_path")

        extraction_result = self.extract_text_from_file(
            file_path=str(file_path),
            max_chars=max_chars
        )

        return {
            "status": extraction_result.get("status"),
            "source_url": url,
            "file_path": file_path,
            "text": extraction_result.get("text"),
            "page_count": extraction_result.get("page_count"),
            "error": extraction_result.get("error")
        }