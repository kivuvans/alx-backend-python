#!/usr/bin/env python3
"""
Task 1: Reusable Query Context Manager
Objective:
    Create a class-based context manager that executes a given SQL query
    and manages both the database connection and query execution.
"""

import sqlite3


class ExecuteQuery:
    """Custom context manager to execute SQL queries safely and efficiently."""

    def __init__(self, db_name, query, params=None):
        """
        Initialize with database name, query, and optional parameters.
        """
        self.db_name = db_name
        self.query = query
        self.params = params or ()
        self.connection = None
        self.cursor = None
        self.results = None

    def __enter__(self):
        """Open the database connection, execute the query, and return results."""
        self.connection = sqlite3.connect(self.db_name)
        self.cursor = self.connection.cursor()
        print(f"Connected to database: {self.db_name}")

        # Execute query
        self.cursor.execute(self.query, self.params)
        self.results = self.cursor.fetchall()
        return self.results

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Ensure the database connection is properly closed."""
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()
            print(f"Closed connection to database: {self.db_name}")
        # Return False to propagate exceptions (if any)
        return False


# ===== Example Usage =====
if __name__ == "__main__":
    query = "SELECT * FROM users WHERE age > ?"
    params = (25,)

    with ExecuteQuery("users.db", query, params) as results:
        print("Query Results:", results)
