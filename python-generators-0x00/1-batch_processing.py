#!/usr/bin/python3
"""
1-batch_processing.py

Generator-based batch processing of user data from MySQL database.
Fetches rows in batches and processes users over the age of 25.
"""

import mysql.connector
from mysql.connector import Error


def stream_users_in_batches(batch_size):
    """
    Generator that fetches user data from MySQL in batches.
    Yields lists (batches) of rows from 'user_data' table.
    """
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='your_mysql_password',  # 🔁 Replace with your MySQL password
            database='ALX_prodev'
        )

        if connection.is_connected():
            cursor = connection.cursor(dictionary=True)
            cursor.execute("SELECT * FROM user_data;")

            batch = []
            for row in cursor:  # loop #1
                batch.append(row)
                if len(batch) == batch_size:
                    yield batch
                    batch = []

            # yield remaining rows if not divisible by batch_size
            if batch:
                yield batch

    except Error as e:
        print(f"Database error: {e}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()


def batch_processing(batch_size):
    """
    Processes users in batches, filters users over age 25,
    and yields each filtered user.
    """
    for batch in stream_users_in_batches(batch_size):  # loop #2
        for user in batch:  # loop #3
            if user["age"] > 25:
                print(user)  # Output directly per 2-main.py behavior
                yield user
