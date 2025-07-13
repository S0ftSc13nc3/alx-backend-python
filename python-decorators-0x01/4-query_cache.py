import time
import sqlite3 
import functools

# Cache dictionary to store query results
query_cache = {}

# Decorator to handle DB connection setup and teardown
def with_db_connection(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        conn = sqlite3.connect('users.db')
        try:
            return func(conn, *args, **kwargs)
        finally:
            conn.close()
    return wrapper

# Decorator to cache query results
def cache_query(func):
    @functools.wraps(func)
    def wrapper(conn, *args, **kwargs):
        # Get query string from keyword or positional argument
        query = kwargs.get('query') or (args[0] if args else None)
        if not query:
            return func(conn, *args, **kwargs)

        if query in query_cache:
            print("Using cached result.")
            return query_cache[query]
        else:
            print("Executing query and caching result.")
            result = func(conn, *args, **kwargs)
            query_cache[query] = result
            return result
    return wrapper

@with_db_connection
@cache_query
def fetch_users_with_cache(conn, query):
    cursor = conn.cursor()
    cursor.execute(query)
    return cursor.fetchall()

# First call will execute and cache
users = fetch_users_with_cache(query="SELECT * FROM users")

# Second call will use the cache
users_again = fetch_users_with_cache(query="SELECT * FROM users")
