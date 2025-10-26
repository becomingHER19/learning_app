# utils/db.py
import sqlite3, datetime
from pathlib import Path

DB_PATH = Path("user_data/learningapp.db")
DB_PATH.parent.mkdir(parents=True, exist_ok=True)

def get_conn():
    conn = sqlite3.connect(str(DB_PATH), check_same_thread=False)
    return conn

def init_db():
    conn = get_conn()
    c = conn.cursor()
    c.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY,
        username TEXT UNIQUE,
        grade TEXT,
        avatar TEXT,
        created_at TEXT
    )""")
    c.execute("""
    CREATE TABLE IF NOT EXISTS events (
        id INTEGER PRIMARY KEY,
        user_id INTEGER,
        kind TEXT,
        details TEXT,
        score REAL,
        created_at TEXT
    )""")
    conn.commit()

def create_user(username, grade, avatar):
    conn = get_conn(); c = conn.cursor()
    now = datetime.datetime.utcnow().isoformat()
    c.execute("INSERT INTO users (username,grade,avatar,created_at) VALUES (?,?,?,?)",
              (username, grade, avatar, now))
    conn.commit()
    return c.lastrowid

def get_user(username):
    conn = get_conn(); c = conn.cursor()
    c.execute("SELECT id,username,grade,avatar FROM users WHERE username=?", (username,))
    return c.fetchone()

def log_event(user_id, kind, details="", score=None):
    conn = get_conn(); c = conn.cursor()
    now = datetime.datetime.utcnow().isoformat()
    c.execute("INSERT INTO events (user_id,kind,details,score,created_at) VALUES (?,?,?,?,?)",
              (user_id, kind, details, score, now))
    conn.commit()

def get_events(user_id, limit=200):
    conn = get_conn(); c = conn.cursor()
    c.execute("SELECT kind,details,score,created_at FROM events WHERE user_id=? ORDER BY id DESC LIMIT ?",
              (user_id, limit))
    return c.fetchall()
