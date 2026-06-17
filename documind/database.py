import json
import sqlite3
import uuid
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional


def get_db_path() -> str:
    db_dir = Path(__file__).resolve().parent.parent / "data"
    db_dir.mkdir(exist_ok=True)
    return str(db_dir / "documind.db")


def get_connection(db_path: str = None) -> sqlite3.Connection:
    conn = sqlite3.connect(db_path or get_db_path())
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA foreign_keys=ON")
    return conn


def init_db(db_path: str = None):
    conn = get_connection(db_path)
    conn.executescript("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE NOT NULL,
            hashed_password TEXT NOT NULL,
            role TEXT NOT NULL DEFAULT 'user',
            created_at TEXT NOT NULL DEFAULT (datetime('now'))
        );

        CREATE TABLE IF NOT EXISTS conversations (
            id TEXT PRIMARY KEY,
            user_id INTEGER NOT NULL,
            title TEXT NOT NULL DEFAULT 'New Chat',
            created_at TEXT NOT NULL DEFAULT (datetime('now')),
            updated_at TEXT NOT NULL DEFAULT (datetime('now')),
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
        );

        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            conversation_id TEXT NOT NULL,
            role TEXT NOT NULL,
            content TEXT NOT NULL,
            sources TEXT,
            created_at TEXT NOT NULL DEFAULT (datetime('now')),
            FOREIGN KEY (conversation_id) REFERENCES conversations(id) ON DELETE CASCADE
        );

        CREATE INDEX IF NOT EXISTS idx_conversations_user ON conversations(user_id);
        CREATE INDEX IF NOT EXISTS idx_messages_conv ON messages(conversation_id);
    """)
    conn.commit()
    conn.close()


class UserDB:
    def __init__(self, db_path: str = None):
        self.db_path = db_path or get_db_path()

    def create_user(self, username: str, email: str, hashed_password: str, role: str = "user") -> Dict:
        conn = get_connection(self.db_path)
        try:
            cur = conn.execute(
                "INSERT INTO users (username, email, hashed_password, role) VALUES (?, ?, ?, ?)",
                (username, email, hashed_password, role),
            )
            conn.commit()
            return self.get_user(cur.lastrowid)
        except sqlite3.IntegrityError as e:
            raise ValueError(f"Username or email already exists: {e}")
        finally:
            conn.close()

    def get_user(self, user_id: int) -> Optional[Dict]:
        conn = get_connection(self.db_path)
        row = conn.execute("SELECT * FROM users WHERE id = ?", (user_id,)).fetchone()
        conn.close()
        return dict(row) if row else None

    def get_user_by_username(self, username: str) -> Optional[Dict]:
        conn = get_connection(self.db_path)
        row = conn.execute("SELECT * FROM users WHERE username = ?", (username,)).fetchone()
        conn.close()
        return dict(row) if row else None

    def get_user_by_email(self, email: str) -> Optional[Dict]:
        conn = get_connection(self.db_path)
        row = conn.execute("SELECT * FROM users WHERE email = ?", (email,)).fetchone()
        conn.close()
        return dict(row) if row else None


class ConversationDB:
    def __init__(self, db_path: str = None):
        self.db_path = db_path or get_db_path()

    def create(self, user_id: int, title: str = "New Chat") -> Dict:
        conn = get_connection(self.db_path)
        conv_id = str(uuid.uuid4())[:8]
        conn.execute(
            "INSERT INTO conversations (id, user_id, title) VALUES (?, ?, ?)",
            (conv_id, user_id, title),
        )
        conn.commit()
        row = conn.execute("SELECT * FROM conversations WHERE id = ?", (conv_id,)).fetchone()
        conn.close()
        return dict(row)

    def list_by_user(self, user_id: int) -> List[Dict]:
        conn = get_connection(self.db_path)
        rows = conn.execute(
            "SELECT * FROM conversations WHERE user_id = ? ORDER BY updated_at DESC",
            (user_id,),
        ).fetchall()
        conn.close()
        return [dict(r) for r in rows]

    def get(self, conv_id: str) -> Optional[Dict]:
        conn = get_connection(self.db_path)
        row = conn.execute("SELECT * FROM conversations WHERE id = ?", (conv_id,)).fetchone()
        conn.close()
        return dict(row) if row else None

    def update_title(self, conv_id: str, title: str):
        conn = get_connection(self.db_path)
        conn.execute(
            "UPDATE conversations SET title = ?, updated_at = datetime('now') WHERE id = ?",
            (title, conv_id),
        )
        conn.commit()
        conn.close()

    def delete(self, conv_id: str):
        conn = get_connection(self.db_path)
        conn.execute("DELETE FROM conversations WHERE id = ?", (conv_id,))
        conn.commit()
        conn.close()

    def add_message(self, conv_id: str, role: str, content: str, sources: List[Dict] = None) -> Dict:
        conn = get_connection(self.db_path)
        sources_json = json.dumps(sources) if sources else None
        cur = conn.execute(
            "INSERT INTO messages (conversation_id, role, content, sources) VALUES (?, ?, ?, ?)",
            (conv_id, role, content, sources_json),
        )
        conn.execute(
            "UPDATE conversations SET updated_at = datetime('now') WHERE id = ?",
            (conv_id,),
        )
        conn.commit()
        row = conn.execute("SELECT * FROM messages WHERE id = ?", (cur.lastrowid,)).fetchone()
        conn.close()
        return dict(row)

    def get_messages(self, conv_id: str) -> List[Dict]:
        conn = get_connection(self.db_path)
        rows = conn.execute(
            "SELECT * FROM messages WHERE conversation_id = ? ORDER BY created_at ASC",
            (conv_id,),
        ).fetchall()
        conn.close()
        result = []
        for r in rows:
            msg = dict(r)
            if msg["sources"]:
                try:
                    msg["sources"] = json.loads(msg["sources"])
                except (json.JSONDecodeError, TypeError):
                    msg["sources"] = []
            result.append(msg)
        return result


init_db()
