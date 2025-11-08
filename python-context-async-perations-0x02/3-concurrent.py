#!/usr/bin/env python3
"""
Task 2: Concurrent Asynchronous Database Queries

Objective:
    Run multiple database queries concurrently using asyncio.gather
    and the aiosqlite library for asynchronous database operations.
"""

import asyncio
import aiosqlite


async def async_fetch_users():
    """Fetch all users asynchronously from the database."""
    async with aiosqlite.connect("users.db") as db:
        async with db.execute("SELECT * FROM users") as cursor:
            results = await cursor.fetchall()
            print("✅ All Users:", results)
            return results


async def async_fetch_older_users():
    """Fetch users older than 40 asynchronously."""
    async with aiosqlite.connect("users.db") as db:
        async with db.execute("SELECT * FROM users WHERE age > 40") as cursor:
            results = await cursor.fetchall()
            print("🧓 Users older than 40:", results)
            return results


async def fetch_concurrently():
    """Run both queries concurrently using asyncio.gather."""
    results = await asyncio.gather(
        async_fetch_users(),
        async_fetch_older_users()
    )
    print("\n🎯 Concurrent query results fetched successfully!")
    return results


if __name__ == "__main__":
    # Run the asynchronous concurrent query execution
    asyncio.run(fetch_concurrently())
