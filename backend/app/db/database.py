"""
KisanSamvaad - SQLite Database Connection Manager
Provides thread-safe connection handling, WAL mode, foreign key constraints,
and automatic schema initialization.
"""

import os
import sqlite3
import threading
from typing import Optional

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
APP_DIR = os.path.dirname(CURRENT_DIR)
BACKEND_DIR = os.path.dirname(APP_DIR)
PROJECT_ROOT = os.path.dirname(BACKEND_DIR)

DEFAULT_DB_PATH = os.path.join(BACKEND_DIR, "kisansamvaad.db")

class DatabaseManager:
    """Manages thread-local SQLite connections and database initialization."""

    _instance: Optional["DatabaseManager"] = None
    _lock = threading.Lock()

    def __init__(self, db_path: Optional[str] = None):
        self.db_path = db_path or os.getenv("DATABASE_PATH", DEFAULT_DB_PATH)
        self._local = threading.local()
        self.init_db()

    @classmethod
    def get_instance(cls, db_path: Optional[str] = None) -> "DatabaseManager":
        with cls._lock:
            if cls._instance is None:
                cls._instance = cls(db_path=db_path)
            return cls._instance

    def get_connection(self) -> sqlite3.Connection:
        """Returns a thread-local SQLite connection."""
        if not hasattr(self._local, "connection") or self._local.connection is None:
            conn = sqlite3.connect(
                self.db_path,
                timeout=10.0,
                check_same_thread=False
            )
            conn.row_factory = sqlite3.Row
            # Enable SQLite Pragmas for concurrency and data integrity
            try:
                conn.execute("PRAGMA journal_mode=WAL;")
                conn.execute("PRAGMA foreign_keys=ON;")
                conn.execute("PRAGMA busy_timeout=5000;")
            except Exception:
                pass
            self._local.connection = conn
        return self._local.connection

    def init_db(self):
        """Executes the DDL schema to ensure tables and indexes exist."""
        schema_file = os.path.join(CURRENT_DIR, "schema.sql")
        if os.path.exists(schema_file):
            with open(schema_file, "r", encoding="utf-8") as f:
                schema_sql = f.read()
            conn = self.get_connection()
            with conn:
                conn.executescript(schema_sql)

    def close_current_thread_connection(self):
        """Closes the connection for the calling thread."""
        if hasattr(self._local, "connection") and self._local.connection:
            try:
                self._local.connection.close()
            except Exception:
                pass
            self._local.connection = None

    def close(self):
        """Closes the active thread connection."""
        self.close_current_thread_connection()

db_manager = DatabaseManager.get_instance()
