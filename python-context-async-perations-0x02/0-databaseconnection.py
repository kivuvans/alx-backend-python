#!/usr/bin/env python3
"""
Task 0: Custom Class-Based Context Manager for Database Connection
Objective:
    Create a class-based context manager to handle opening and closing
    database connections automatically.
"""

import sqlite3


class DatabaseConnection:
    """Custom context manager for managing SQLite database connections."""

    def __init__(self, db_name):
        """Initialize the context manager with the database name."""
        self.db_name = db_name
        self.connection = None

    def __enter__(self):
        """Establish and return the database connection."""
        self.connection = sqlite3.connect(self.db_name)
        print(f"Connected to database: {self.db_name}")
        return self.connection

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Ensure the database connection is properly closed."""
        if self.connection:
            self.connection.close()
            print(f"Closed connection to database: {self.db_name}")


# ===== Example usage =====
if __name__ == "__main__":
    with DatabaseConnection("users.db") as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users")
        results = cursor.fetchall()
        print("Query Results:", results)
