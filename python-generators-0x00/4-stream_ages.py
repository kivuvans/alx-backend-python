#!/usr/bin/python3
"""
4-stream_ages.py

Objective:
Use a generator to compute a memory-efficient average age
from the user_data table without loading the full dataset into memory.
"""

import seed


def stream_user_ages():
    """
    Generator that yields user ages one by one from the database.
    Uses minimal memory by streaming results instead of fetching all at once.
    """
    connection = seed.connect_to_prodev()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT age FROM user_data")

    for row in cursor:
        yield row["age"]

    cursor.close()
    connection.close()


def calculate_average_age():
    """
    Uses the stream_user_ages generator to compute the average age
    without loading the full dataset into memory.
    """
    total = 0
    count = 0

    for age in stream_user_ages():
        total += age
        count += 1

    if count == 0:
        print("No users found.")
        return

    average = total / count
    print(f"Average age of users: {average:.2f}")


if __name__ == "__main__":
    calculate_average_age()
