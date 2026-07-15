import sqlite3
import json
import os
import time
from typing import Optional, Dict, Any

class IdempotencyStore:
    """
    SQLite-backed store to guarantee step idempotency.
    If a workflow step crashes midway or is re-executed, this ensures external actions 
    (like publishing a product) aren't duplicated.
    """
    
    def __init__(self, db_path: str = ".system_generated/idempotency.db"):
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        self.db_path = db_path
        self._init_db()
        
    def _init_db(self):
        with sqlite3.connect(self.db_path) as conn:
            conn.execute('''
                CREATE TABLE IF NOT EXISTS idempotency_keys (
                    key_id TEXT PRIMARY KEY,
                    result TEXT,
                    completed_at REAL
                )
            ''')
            conn.commit()
            
    def get(self, idempotency_key: str) -> Optional[Dict[str, Any]]:
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute(
                "SELECT result FROM idempotency_keys WHERE key_id = ?", 
                (idempotency_key,)
            )
            row = cursor.fetchone()
            if row:
                return json.loads(row[0])
        return None
        
    def set(self, idempotency_key: str, result: Dict[str, Any]):
        with sqlite3.connect(self.db_path) as conn:
            conn.execute(
                "INSERT OR REPLACE INTO idempotency_keys (key_id, result, completed_at) VALUES (?, ?, ?)",
                (idempotency_key, json.dumps(result), time.time())
            )
            conn.commit()
