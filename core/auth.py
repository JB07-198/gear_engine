import os
from typing import Optional, Dict, Any
from passlib.hash import bcrypt
import jwt
import time
from core.export_db import _get_conn

JWT_SECRET = os.environ.get('JWT_SECRET', 'change-me')
JWT_ALGO = 'HS256'
JWT_EXP_SECONDS = int(os.environ.get('JWT_EXP', '604800'))  # 7 days


def _get_user(username: str) -> Optional[Dict[str, Any]]:
    conn = _get_conn()
    cur = conn.cursor()
    cur.execute("SELECT username, password_hash FROM users WHERE username = ?", (username,))
    row = cur.fetchone()
    conn.close()
    if not row:
        return None
    return dict(row)


def register_user(username: str, password: str) -> str:
    pw_hash = bcrypt.hash(password)
    conn = _get_conn()
    cur = conn.cursor()
    cur.execute("INSERT OR REPLACE INTO users (username, password_hash) VALUES (?, ?)", (username, pw_hash))
    conn.commit()
    conn.close()
    return generate_token(username)


def authenticate_user(username: str, password: str) -> Optional[str]:
    user = _get_user(username)
    if not user:
        return None
    if bcrypt.verify(password, user['password_hash']):
        return generate_token(username)
    return None


def generate_token(username: str) -> str:
    payload = {
        'sub': username,
        'iat': int(time.time()),
        'exp': int(time.time()) + JWT_EXP_SECONDS,
    }
    return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGO)


def verify_token(token: str) -> Optional[str]:
    try:
        data = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGO])
        return data.get('sub')
    except Exception:
        return None
