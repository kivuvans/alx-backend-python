#!/usr/bin/python3
"""
2-lazy_paginate.py

Implements lazy pagination using generators.
Simulates fetching paginated user data from the ALX_prodev MySQL database.
"""

import seed


def paginate_users(page_size, offset):
    """
    Fetch a single page of users from the user_data table
    using LIMIT and OFFSET.
    """
    connection = seed.connect_to_prodev()
    cursor = connection.cursor(dictionary=True)
    cursor.execute(f"SELECT * FROM user_data LIMIT {page_size} OFFSET {offset}")
    rows = cursor.fetchall()
    connection.close()
    return rows


def lazy_pagination(page_size):
    """
    Lazily loads each page from the database using a generator.
    Fetches the next page only when requested (lazy loading).
    Uses only one loop.
    """
    offset = 0
    while True:  # ✅ Only one loop
        page = paginate_users(page_size, offset)
        if not page:
            break
        yield page  # yield one page at a time
        offset += page_size
