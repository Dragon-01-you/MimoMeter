import sqlite3
import os
import csv
import json
from datetime import datetime

DB_PATH = os.path.join(os.path.expanduser("~"), ".mimo-meter", "usage.db")

def init_db():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.execute('''
        CREATE TABLE IF NOT EXISTS usage (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            model TEXT,
            prompt_tokens INTEGER DEFAULT 0,
            completion_tokens INTEGER DEFAULT 0,
            total_tokens INTEGER DEFAULT 0,
            status TEXT
        )
    ''')
    conn.commit()
    return conn

def record_usage(model, prompt, completion, total, status="success"):
    conn = sqlite3.connect(DB_PATH)
    conn.execute('''
        INSERT INTO usage (timestamp, model, prompt_tokens, completion_tokens, total_tokens, status)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (datetime.now().isoformat(), model, prompt, completion, total, status))
    conn.commit()
    conn.close()

def get_stats():
    conn = sqlite3.connect(DB_PATH)
    today = conn.execute('''
        SELECT SUM(prompt_tokens), SUM(completion_tokens), SUM(total_tokens), COUNT(*)
        FROM usage WHERE date(timestamp) = date('now')
    ''').fetchone()
    total = conn.execute('''
        SELECT SUM(prompt_tokens), SUM(completion_tokens), SUM(total_tokens), COUNT(*)
        FROM usage
    ''').fetchone()
    by_model = conn.execute('''
        SELECT model, SUM(total_tokens), COUNT(*) FROM usage GROUP BY model
    ''').fetchall()
    trend = conn.execute('''
        SELECT date(timestamp) as day, SUM(total_tokens)
        FROM usage WHERE timestamp > datetime('now', '-7 days')
        GROUP BY day ORDER BY day
    ''').fetchall()
    recent = conn.execute('''
        SELECT timestamp, model, prompt_tokens, completion_tokens, total_tokens, status
        FROM usage ORDER BY id DESC LIMIT 10
    ''').fetchall()
    conn.close()
    return {
        "today": {"prompt": today[0] or 0, "completion": today[1] or 0, "total": today[2] or 0, "calls": today[3] or 0},
        "total": {"prompt": total[0] or 0, "completion": total[1] or 0, "total": total[2] or 0, "calls": total[3] or 0},
        "by_model": [{"model": m, "tokens": t, "calls": c} for m, t, c in by_model],
        "trend": [{"date": d, "tokens": t} for d, t in trend],
        "recent": [{"timestamp": r[0], "model": r[1], "prompt": r[2], "completion": r[3], "total": r[4], "status": r[5]} for r in recent]
    }

def export_csv():
    conn = sqlite3.connect(DB_PATH)
    rows = conn.execute('''
        SELECT timestamp, model, prompt_tokens, completion_tokens, total_tokens, status
        FROM usage ORDER BY id DESC
    ''').fetchall()
    conn.close()
    return rows

def export_json():
    conn = sqlite3.connect(DB_PATH)
    rows = conn.execute('''
        SELECT timestamp, model, prompt_tokens, completion_tokens, total_tokens, status
        FROM usage ORDER BY id DESC
    ''').fetchall()
    conn.close()
    return [{"timestamp": r[0], "model": r[1], "prompt_tokens": r[2], "completion_tokens": r[3], "total_tokens": r[4], "status": r[5]} for r in rows]
