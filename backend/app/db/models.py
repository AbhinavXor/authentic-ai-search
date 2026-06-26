"""
=========================================================
MODULE: Database Models

Project:
Authentic AI Search

Purpose:
Create SQLite tables for query history and feedback.

Author:
Abhinav

Version:
1.0.0
=========================================================
"""

from backend.app.db.database import get_connection


def initialize_database() -> None:
    """
    Create required database tables.
    """

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS query_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            query_text TEXT NOT NULL,
            answer TEXT,
            trust_score REAL,
            verification_status TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """
    )

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS feedback (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            query_text TEXT NOT NULL,
            rating INTEGER,
            comment TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """
    )

    connection.commit()
    connection.close()