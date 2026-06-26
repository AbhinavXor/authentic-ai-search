"""
=========================================================
MODULE: Feedback Store

Project:
Authentic AI Search

Purpose:
Persist user feedback records in SQLite.

Author:
Abhinav

Version:
1.0.0
=========================================================
"""

import json
import sqlite3
from pathlib import Path
from typing import Any, Dict, List


class FeedbackStore:
    """
    SQLite storage for feedback records.
    """

    def __init__(
        self,
        db_path: str = "data/feedback.db"
    ) -> None:
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        self._create_table()

    def _connect(self) -> sqlite3.Connection:
        return sqlite3.connect(
            self.db_path
        )

    def _create_table(self) -> None:
        with self._connect() as connection:
            cursor = connection.cursor()

            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS feedback (
                    feedback_id TEXT PRIMARY KEY,
                    answer_id TEXT,
                    query TEXT NOT NULL,
                    answer TEXT NOT NULL,
                    feedback_type TEXT NOT NULL,
                    feedback_weight REAL NOT NULL,
                    user_comment TEXT,
                    metadata TEXT,
                    created_at TEXT NOT NULL
                )
                """
            )

            connection.commit()

    def save(
        self,
        feedback_record: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Save feedback record.
        """

        with self._connect() as connection:
            cursor = connection.cursor()

            cursor.execute(
                """
                INSERT INTO feedback (
                    feedback_id,
                    answer_id,
                    query,
                    answer,
                    feedback_type,
                    feedback_weight,
                    user_comment,
                    metadata,
                    created_at
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    feedback_record.get("feedback_id"),
                    feedback_record.get("answer_id"),
                    feedback_record.get("query"),
                    feedback_record.get("answer"),
                    feedback_record.get("feedback_type"),
                    feedback_record.get("feedback_weight"),
                    feedback_record.get("user_comment"),
                    json.dumps(
                        feedback_record.get("metadata", {})
                    ),
                    feedback_record.get("created_at")
                )
            )

            connection.commit()

        return feedback_record

    def list_recent(
        self,
        limit: int = 20
    ) -> List[Dict[str, Any]]:
        """
        Return recent feedback records.
        """

        with self._connect() as connection:
            connection.row_factory = sqlite3.Row
            cursor = connection.cursor()

            cursor.execute(
                """
                SELECT *
                FROM feedback
                ORDER BY created_at DESC
                LIMIT ?
                """,
                (limit,)
            )

            rows = cursor.fetchall()

        results = []

        for row in rows:
            item = dict(row)

            try:
                item["metadata"] = json.loads(
                    item.get("metadata") or "{}"
                )
            except Exception:
                item["metadata"] = {}

            results.append(item)

        return results