#(©)CodeXBotz

import psycopg2
from psycopg2.extras import RealDictCursor
from config import DB_URI
import os

def get_db_connection():
    return psycopg2.connect(DB_URI)

async def present_user(user_id: int):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT user_id FROM users WHERE user_id = %s", (user_id,))
        result = cursor.fetchone()
        cursor.close()
        conn.close()
        return bool(result)
    except Exception as e:
        print(f"Error checking user: {e}")
        return False

async def add_user(user_id: int):
    """Add user with ON CONFLICT handling - does nothing if user exists"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO users (user_id) VALUES (%s) ON CONFLICT (user_id) DO NOTHING",
            (user_id,)
        )
        conn.commit()
        cursor.close()
        conn.close()
    except Exception as e:
        print(f"Error adding user: {e}")

async def add_user_with_timestamp(user_id: int):
    """Add user and update timestamp if already exists"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO users (user_id, joined_date) 
            VALUES (%s, NOW()) 
            ON CONFLICT (user_id) 
            DO UPDATE SET last_seen = NOW()
        """, (user_id,))
        conn.commit()
        cursor.close()
        conn.close()
    except Exception as e:
        print(f"Error adding/updating user: {e}")

async def upsert_user(user_id: int, username: str | None = None, first_name: str | None = None):
    """Insert or update user with all available information"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO users (user_id, username, first_name, joined_date) 
            VALUES (%s, %s, %s, NOW()) 
            ON CONFLICT (user_id) 
            DO UPDATE SET 
                username = EXCLUDED.username,
                first_name = EXCLUDED.first_name,
                last_seen = NOW()
        """, (user_id, username, first_name))
        conn.commit()
        cursor.close()
        conn.close()
    except Exception as e:
        print(f"Error upserting user: {e}")

async def full_userbase():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT user_id FROM users")
        user_ids = [row[0] for row in cursor.fetchall()]
        cursor.close()
        conn.close()
        return user_ids
    except Exception as e:
        print(f"Error fetching userbase: {e}")
        return []

async def del_user(user_id: int):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM users WHERE user_id = %s", (user_id,))
        conn.commit()
        cursor.close()
        conn.close()
    except Exception as e:
        print(f"Error deleting user: {e}")