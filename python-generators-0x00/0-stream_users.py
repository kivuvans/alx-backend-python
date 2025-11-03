#!/usr/bin/python3
"""
0-stream_users.py

A generator function that streams rows from the MySQL database `ALX_prodev`
table `user_data` one by one using Python's `yield`.
"""

import mysql.connector
from mysql.connector import Error


def stream_users():
    """Generator that fetches user_data rows one by one from MySQL."""
    try:
        # Connect to the ALX_prodev database
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='your_mysql_password',  # 🔁 Replace with your MySQL password
            database='ALX_prodev'
        )

        if connection.is_connected():
            cursor = connection.cursor(dictionary=True)
            cursor.execute("SELECT * FROM user_data;")

            # Use a single loop to yield each row
            for row in cursor:
                yield {
                    "user_id": row["user_id"],
                    "name": row["name"],
                    "email": row["email"],
                    "age": row["age"]
                }

    except Error as e:
        print(f"Database error: {e}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
