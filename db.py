import sqlite3
import os
import base64
import requests
from config import DB_PATH


def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS published_news (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            url TEXT UNIQUE,
            title TEXT,
            source TEXT,
            published_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()


def _push_db():
    token = os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")
    if not token:
        return
    repo = os.environ.get("GITHUB_REPOSITORY", "VAYakushev/auto-news-bot")
    try:
        with open(DB_PATH, "rb") as f:
            content = base64.b64encode(f.read()).decode()
        r = requests.get(f"https://api.github.com/repos/{repo}/contents/{DB_PATH}",
            headers={"Authorization": f"Bearer {token}"})
        if r.status_code == 200:
            sha = r.json()["sha"]
            body = {"message": "Update news.db", "content": content, "sha": sha}
        else:
            body = {"message": "Add news.db", "content": content}
        requests.put(f"https://api.github.com/repos/{repo}/contents/{DB_PATH}",
            headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"},
            json=body)
    except Exception:
        pass


def is_already_published(url: str, title: str = "") -> bool:
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT url, title FROM published_news")
    for row in cursor.fetchall():
        if row[0] == url:
            conn.close()
            return True
        if title and row[1] and levenshtein_distance(row[1].lower(), title.lower()) < 5:
            conn.close()
            return True
    conn.close()
    return False


def levenshtein_distance(s1: str, s2: str) -> int:
    if len(s1) < len(s2):
        return levenshtein_distance(s2, s1)
    if len(s2) == 0:
        return len(s1)
    
    previous_row = range(len(s2) + 1)
    for i, c1 in enumerate(s1):
        current_row = [i + 1]
        for j, c2 in enumerate(s2):
            insertions = previous_row[j + 1] + 1
            deletions = current_row[j] + 1
            substitutions = previous_row[j] + (c1 != c2)
            current_row.append(min(insertions, deletions, substitutions))
        previous_row = current_row
    
    return previous_row[-1]


def mark_as_published(url: str, title: str, source: str):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO published_news (url, title, source) VALUES (?, ?, ?)",
            (url, title, source)
        )
        conn.commit()
    except sqlite3.IntegrityError:
        pass
    finally:
        conn.close()
    _push_db()


init_db()