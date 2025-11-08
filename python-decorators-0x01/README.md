# Python Decorators – Database Operations Project

## Overview
This project demonstrates the use of Python decorators to improve database operations through clean, reusable, and maintainable code. Each task builds upon the previous to simulate real-world backend development.

## Tasks
### 0. Logging Database Queries
Decorator: `@log_queries`  
Logs SQL queries before execution.

### 1. Handle Database Connections
Decorator: `@with_db_connection`  
Automatically manages database connections and ensures clean-up.

### 2. Transaction Management
Decorator: `@transactional`  
Commits successful transactions or rolls back upon errors.

### 3. Retry Database Queries
Decorator: `@retry_on_failure(retries=3, delay=1)`  
Retries database operations on transient errors.

### 4. Cache Database Queries
Decorator: `@cache_query`  
Caches SQL query results to reduce redundant database hits.

## Technologies Used
- Python 3.8+
- SQLite3
- functools
- time

## Author
**Evans Kivuva**
