import sqlite3
import os
from datetime import datetime

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "responses.db")


def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_connection()
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS provid_responses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            telegram TEXT,
            phone TEXT,
            tasks TEXT,
            idea TEXT,
            about TEXT,
            created_at TEXT NOT NULL
        )
        """
    )
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS lecturer_responses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            telegram TEXT,
            phone TEXT,
            talks TEXT,
            own_topic TEXT,
            experience TEXT,
            created_at TEXT NOT NULL
        )
        """
    )
    conn.commit()
    conn.close()


def _now():
    return datetime.now().strftime("%Y-%m-%d %H:%M")


def insert_provid_response(name, telegram, phone, tasks, idea, about):
    conn = get_connection()
    conn.execute(
        "INSERT INTO provid_responses (name, telegram, phone, tasks, idea, about, created_at) "
        "VALUES (?, ?, ?, ?, ?, ?, ?)",
        (name, telegram, phone, ", ".join(tasks), idea, about, _now()),
    )
    conn.commit()
    conn.close()


def insert_lecturer_response(name, telegram, phone, talks, own_topic, experience):
    conn = get_connection()
    conn.execute(
        "INSERT INTO lecturer_responses (name, telegram, phone, talks, own_topic, experience, created_at) "
        "VALUES (?, ?, ?, ?, ?, ?, ?)",
        (name, telegram, phone, ", ".join(talks), own_topic, experience, _now()),
    )
    conn.commit()
    conn.close()


def get_provid_responses():
    conn = get_connection()
    rows = conn.execute("SELECT * FROM provid_responses ORDER BY id DESC").fetchall()
    conn.close()
    return rows


def get_lecturer_responses():
    conn = get_connection()
    rows = conn.execute("SELECT * FROM lecturer_responses ORDER BY id DESC").fetchall()
    conn.close()
    return rows
