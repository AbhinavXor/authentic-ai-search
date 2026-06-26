"""
=========================================================
MODULE: Table Extractor

Project:
Authentic AI Search

Engine:
VRA Search Engine

Purpose:
Extract simple HTML tables from fetched source content.

Author:
Abhinav

Version:
1.0.0
=========================================================
"""

from typing import Any, Dict, List

from bs4 import BeautifulSoup


class TableExtractor:
    """
    Extracts structured table data from HTML content.

    This module is intentionally independent.
    It will be integrated into pipeline.py later.
    """

    def __init__(
        self,
        max_tables: int = 5,
        max_rows_per_table: int = 30
    ) -> None:
        self.max_tables = max_tables
        self.max_rows_per_table = max_rows_per_table

    def _clean_cell(
        self,
        value: str
    ) -> str:
        """
        Clean table cell text.
        """

        return " ".join(
            value.split()
        ).strip()

    def _extract_table(
        self,
        table
    ) -> Dict[str, Any]:
        """
        Extract one HTML table.
        """

        rows: List[List[str]] = []

        for row in table.find_all("tr"):
            cells = row.find_all(
                ["th", "td"]
            )

            cell_values = [
                self._clean_cell(
                    cell.get_text(" ", strip=True)
                )
                for cell in cells
            ]

            if cell_values:
                rows.append(cell_values)

            if len(rows) >= self.max_rows_per_table:
                break

        if not rows:
            return {
                "headers": [],
                "rows": []
            }

        headers = rows[0]
        body_rows = rows[1:]

        return {
            "headers": headers,
            "rows": body_rows
        }

    def extract_from_html(
        self,
        html: str
    ) -> List[Dict[str, Any]]:
        """
        Extract tables from raw HTML.
        """

        if not html:
            return []

        soup = BeautifulSoup(
            html,
            "lxml"
        )

        html_tables = soup.find_all("table")

        extracted_tables = []

        for table in html_tables[: self.max_tables]:
            extracted = self._extract_table(
                table
            )

            if extracted.get("headers") or extracted.get("rows"):
                extracted_tables.append(extracted)

        return extracted_tables

    def extract(
        self,
        record: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Extract tables from evidence record.
        """

        html_content = (
            record.get("raw_html")
            or record.get("html")
            or record.get("content")
            or ""
        )

        tables = self.extract_from_html(
            html_content
        )

        return {
            "tables": tables,
            "table_count": len(tables),
            "has_tables": len(tables) > 0
        }

    def enrich_records(
        self,
        evidence_records: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """
        Add table information to evidence records.
        """

        updated_records = []

        for record in evidence_records:
            result = self.extract(record)

            record["tables"] = result.get("tables", [])
            record["table_count"] = result.get("table_count", 0)
            record["has_tables"] = result.get("has_tables", False)

            updated_records.append(record)

        return updated_records