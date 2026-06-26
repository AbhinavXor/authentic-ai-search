"""
=========================================================
MODULE: Query History Repository

Project:
Authentic AI Search

Purpose:
Save user query history.

Author:
Abhinav

Version:
1.0.0
=========================================================
"""

from typing import Optional

from backend.app.db.database import get_connection


def save_query_history(
    query_text: str,
    answer: str,
    trust_score: float,
    verification_status: str
) -> Optional[int]:
    """
    Save query result to database.
    """

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO query_history (
            query_text,
            answer,
            trust_score,
            verification_status
        )
        VALUES (?, ?, ?, ?)
        """,
        (
            query_text,
            answer,
            trust_score,
            verification_status
        )
    )

    connection.commit()

    row_id = cursor.lastrowid

    connection.close()

    return row_id