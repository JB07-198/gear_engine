"""Lightweight SQLite job storage for export jobs."""
import sqlite3
import threading
from typing import Optional, Dict, Any

DB_PATH = "gear_exports.db"
_init_lock = threading.Lock()


def _get_conn():
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    with _init_lock:
        conn = _get_conn()
        cur = conn.cursor()
        cur.execute("""
        CREATE TABLE IF NOT EXISTS jobs (
            job_id TEXT PRIMARY KEY,
            status TEXT,
            filename TEXT,
            format TEXT,
            token TEXT,
            username TEXT,
            error TEXT
        )
        """)
        # users table for auth (password hash stored)
        cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            username TEXT PRIMARY KEY,
            password_hash TEXT
        )
        """)
        conn.commit()
        conn.close()


def add_job(job_id: str, filename: str, fmt: str, token: Optional[str] = None, username: Optional[str] = None):
    conn = _get_conn()
    cur = conn.cursor()
    cur.execute(
        "INSERT OR REPLACE INTO jobs (job_id, status, filename, format, token, username) VALUES (?, ?, ?, ?, ?, ?)",
        (job_id, 'pending', filename, fmt, token, username),
    )
    conn.commit()
    conn.close()


def update_job_status(job_id: str, status: str, error: Optional[str] = None):
    conn = _get_conn()
    cur = conn.cursor()
    cur.execute("UPDATE jobs SET status = ?, error = ? WHERE job_id = ?", (status, error, job_id))
    conn.commit()
    conn.close()


def get_job(job_id: str) -> Optional[Dict[str, Any]]:
    conn = _get_conn()
    cur = conn.cursor()
    cur.execute("SELECT job_id, status, filename, format, token, username, error FROM jobs WHERE job_id = ?", (job_id,))
    row = cur.fetchone()
    conn.close()
    if not row:
        return None
    return dict(row)


def list_jobs(username: Optional[str] = None) -> list:
    conn = _get_conn()
    cur = conn.cursor()
    if username:
        cur.execute("SELECT job_id, status, filename, format, token, username, error FROM jobs WHERE username = ?", (username,))
    else:
        cur.execute("SELECT job_id, status, filename, format, token, username, error FROM jobs")
    rows = cur.fetchall()
    conn.close()
    return [dict(r) for r in rows]


def revoke_job(job_id: str) -> bool:
    conn = _get_conn()
    cur = conn.cursor()
    cur.execute("UPDATE jobs SET status = ? WHERE job_id = ?", ('revoked', job_id))
    changed = cur.rowcount
    conn.commit()
    conn.close()
    return changed > 0


### User management ###
import hashlib


# Note: user management (registration/authentication) is handled in core.auth
