"""
=========================================================
MODULE: Feedback Repository

Project:
Authentic AI Search

Purpose:
Store user feedback.

Author:
Abhinav

Version:
1.0.0
=========================================================
"""

from typing import Optional

from backend.app.db.database import get_connection


def save_feedback(
    query_text: str,
    rating: int,
    comment: str = ""
) -> Optional[int]:
    """
    Save feedback entry.
    """

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO feedback (
            query_text,
            rating,
            comment
        )
        VALUES (?, ?, ?)
        """,
        (
            query_text,
            rating,
            comment
        )
    )

    connection.commit()

    row_id = cursor.lastrowid

    connection.close()

    return row_id