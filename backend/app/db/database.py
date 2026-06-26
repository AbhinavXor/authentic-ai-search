"""
=========================================================
MODULE: Database Connection

Project:
Authentic AI Search

Purpose:
SQLite database setup.

Author:
Abhinav

Version:
1.0.0
=========================================================
"""

import sqlite3
from pathlib import Path


DATABASE_PATH = Path("data/authentic_ai_search.db")


def get_connection() -> sqlite3.Connection:
    """
    Return SQLite database connection.
    """

    DATABASE_PATH.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    connection = sqlite3.connect(
        DATABASE_PATH
    )

    connection.row_factory = sqlite3.Row

    return connection