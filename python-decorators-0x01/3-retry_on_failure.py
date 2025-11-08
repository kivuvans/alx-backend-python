
3. Using Decorators to retry database queries
mandatory
Objective: create a decorator that retries database operations if they fail due to transient errors

Instructions:

Complete the script below by implementing a retry_on_failure(retries=3, delay=2) decorator that retries the function of a certain number of times if it raises an exception
import time
import sqlite3 
import functools

#### paste your with_db_decorator here

""" your code goes here"""

@with_db_connection
@retry_on_failure(retries=3, delay=1)

def fetch_users_with_retry(conn):
cursor = conn.cursor()
cursor.execute("SELECT * FROM users")
return cursor.fetchall()

#### attempt to fetch users with automatic retry on failure

users = fetch_users_with_retry()
print(users)
Repo:

GitHub repository: alx-backend-python
Directory: python-decorators-0x01
File: 3-retry_on_failure.py
