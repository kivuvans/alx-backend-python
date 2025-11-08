
#!/usr/bin/python3
import sqlite3
import functools

# Global cache dictionary to store query results
query_cache = {}


def with_db_connection(func):
    """Decorator that opens a DB connection, passes it to the function, and closes it afterward."""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        conn = sqlite3.connect('users.db')
        try:
            result = func(conn, *args, **kwargs)
        finally:
            conn.close()
        return result
    return wrapper


def cache_query(func):
    """Decorator that caches query results based on the SQL query string."""
    @functools.wraps(func)
    def wrapper(conn, query, *args, **kwargs):
        # Use the SQL query as the cache key
        if query in query_cache:
            print(f"✅ Using cached result for query: {query}")
            return query_cache[query]

        # If not cached, execute and cache the result
        print(f"🕓 Executing and caching new result for query: {query}")
        result = func(conn, query, *args, **kwargs)
        query_cache[query] = result
        return result
    return wrapper


@with_db_connection
@cache_query
def fetch_users_with_cache(conn, query):
    """Fetch users with caching to avoid redundant DB calls."""
    cursor = conn.cursor()
    cursor.execute(query)
    return cursor.fetchall()


# ✅ First call will execute and cache the result
users = fetch_users_with_cache(query="SELECT * FROM users")

# ✅ Second call will use the cached result
users_again = fetch_users_with_cache(query="SELECT * FROM users")
