"""
=========================================================
MODULE: Source Stats Store

Project:
Authentic AI Search

Purpose:
Persist source-level feedback statistics.

Author:
Abhinav

Version:
1.0.0
=========================================================
"""

import sqlite3
from pathlib import Path
from typing import Any, Dict, Optional


class SourceStatsStore:
    """
    SQLite storage for source-level feedback stats.
    """

    def __init__(
        self,
        db_path: str = "data/source_stats.db"
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
                CREATE TABLE IF NOT EXISTS source_stats (
                    domain TEXT PRIMARY KEY,
                    source_name TEXT,
                    upvotes INTEGER DEFAULT 0,
                    downvotes INTEGER DEFAULT 0,
                    reports INTEGER DEFAULT 0,
                    total_feedback INTEGER DEFAULT 0,
                    feedback_score REAL DEFAULT 50.0
                )
                """
            )

            connection.commit()

    def update_feedback_stats(
        self,
        domain: str,
        source_name: Optional[str],
        feedback_type: str
    ) -> Dict[str, Any]:
        """
        Update source stats from feedback.
        """

        if not domain:
            return {}

        feedback_type = (
            feedback_type.strip().lower()
            if feedback_type
            else "neutral"
        )

        with self._connect() as connection:
            connection.row_factory = sqlite3.Row
            cursor = connection.cursor()

            cursor.execute(
                """
                INSERT OR IGNORE INTO source_stats (
                    domain,
                    source_name
                )
                VALUES (?, ?)
                """,
                (
                    domain,
                    source_name
                )
            )

            if feedback_type == "upvote":
                cursor.execute(
                    """
                    UPDATE source_stats
                    SET upvotes = upvotes + 1,
                        total_feedback = total_feedback + 1
                    WHERE domain = ?
                    """,
                    (domain,)
                )

            elif feedback_type == "downvote":
                cursor.execute(
                    """
                    UPDATE source_stats
                    SET downvotes = downvotes + 1,
                        total_feedback = total_feedback + 1
                    WHERE domain = ?
                    """,
                    (domain,)
                )

            elif feedback_type == "report":
                cursor.execute(
                    """
                    UPDATE source_stats
                    SET reports = reports + 1,
                        total_feedback = total_feedback + 1
                    WHERE domain = ?
                    """,
                    (domain,)
                )

            cursor.execute(
                """
                SELECT *
                FROM source_stats
                WHERE domain = ?
                """,
                (domain,)
            )

            row = cursor.fetchone()

            if not row:
                connection.commit()
                return {}

            upvotes = int(row["upvotes"])
            downvotes = int(row["downvotes"])
            reports = int(row["reports"])
            total_feedback = int(row["total_feedback"])

            if total_feedback > 0:
                feedback_score = (
                    50.0
                    + upvotes * 5.0
                    - downvotes * 8.0
                    - reports * 15.0
                )

                feedback_score = max(
                    0.0,
                    min(feedback_score, 100.0)
                )
            else:
                feedback_score = 50.0

            cursor.execute(
                """
                UPDATE source_stats
                SET feedback_score = ?
                WHERE domain = ?
                """,
                (
                    feedback_score,
                    domain
                )
            )

            connection.commit()

            cursor.execute(
                """
                SELECT *
                FROM source_stats
                WHERE domain = ?
                """,
                (domain,)
            )

            updated_row = cursor.fetchone()

        return dict(updated_row) if updated_row else {}

    def get_source_stats(
        self,
        domain: str
    ) -> Dict[str, Any]:
        """
        Get stats for a source domain.
        """

        with self._connect() as connection:
            connection.row_factory = sqlite3.Row
            cursor = connection.cursor()

            cursor.execute(
                """
                SELECT *
                FROM source_stats
                WHERE domain = ?
                """,
                (domain,)
            )

            row = cursor.fetchone()

        return dict(row) if row else {}

    def list_sources(self) -> list[Dict[str, Any]]:
        """
        List all source stats.
        """

        with self._connect() as connection:
            connection.row_factory = sqlite3.Row
            cursor = connection.cursor()

            cursor.execute(
                """
                SELECT *
                FROM source_stats
                ORDER BY feedback_score DESC
                """
            )

            rows = cursor.fetchall()

        return [
            dict(row)
            for row in rows
        ]