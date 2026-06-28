from __future__ import annotations

import sqlite3
from pathlib import Path
from typing import List, Dict, Any


class CustomerMemory:
    def __init__(self, db_path: str | Path = "memory.db") -> None:
        self.db_path = Path(db_path)
        self._initialize_db()

    def _initialize_db(self) -> None:
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        with sqlite3.connect(self.db_path) as conn:
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS conversations (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    customer_id TEXT NOT NULL,
                    role TEXT NOT NULL,
                    message TEXT NOT NULL,
                    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
                )
                """
            )
            conn.commit()

    def store_message(self, customer_id: str, role: str, message: str) -> None:
        with sqlite3.connect(self.db_path) as conn:
            conn.execute(
                "INSERT INTO conversations (customer_id, role, message) VALUES (?, ?, ?)",
                (customer_id, role, message),
            )
            conn.commit()

    def get_history(self, customer_id: str) -> List[Dict[str, Any]]:
        with sqlite3.connect(self.db_path) as conn:
            rows = conn.execute(
                "SELECT role, message FROM conversations WHERE customer_id = ? ORDER BY id",
                (customer_id,),
            ).fetchall()
        return [{"role": role, "message": message} for role, message in rows]

    def get_last_issue(self, customer_id: str) -> str | None:
        history = self.get_history(customer_id)
        for item in reversed(history):
            if item["role"] == "customer":
                return item["message"]
        return None
