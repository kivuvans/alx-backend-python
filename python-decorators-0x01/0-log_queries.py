#!/usr/bin/python3
import sqlite3
import functools

# Decorator to log SQL queries
def log_queries(func):
    """Decorator that logs the SQL query before executing it."""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # Extract query from args or kwargs
        query = kwargs.get("query") if "query" in kwargs else args[0] if args else None
        
        if query:
            print(f"[LOG] Executing SQL Query: {query}")
        else:
            print("[LOG] No query found to execute.")
        
        # Call the actual function
        return func(*args, **kwargs)
    
    return wrapper


@log_queries
def fetch_all_users(query):
    """Fetch all users from the database."""
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute(query)
    results = cursor.fetchall()
    conn.close()
    return results


# Example usage
if __name__ == "__main__":
    users = fetch_all_users(query="SELECT * FROM users")
    print(users)
