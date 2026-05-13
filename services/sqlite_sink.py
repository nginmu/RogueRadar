# This is /services/sqlite_sink.py
# RR V3 iteration 001
#
# Written by ChatGPT & Claude
# Steered by Nginmu Mbetse
# May 7 2026

import sqlite3
import json
import threading
import time

class SQLiteSink:

    def __init__(self, db_path="events.db"):

        self.db_path = db_path
        self.enabled = False

        self.conn = None
        self.lock = threading.Lock()

    # LIFECYCLE
    def start(self):

        if self.enabled:
            return

        self.conn = sqlite3.connect(self.db_path, check_same_thread=False)
        self._init_db()
        self.enabled = True
        print("SQLiteSink: ENABLED")

    def stop(self):

        if not self.enabled:
            return

        try:
            self.conn.close()
        except Exception:
            pass

        self.enabled = False
        print("SQLiteSink: DISABLED")

    def toggle(self):

        if self.enabled:
            self.stop()
        else:
            self.start()

    # DB SETUP
    def _init_db(self):

        with self.conn:
            self.conn.execute("""
                CREATE TABLE IF NOT EXISTS events (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    ts REAL,
                    source TEXT,
                    type TEXT,
                    payload TEXT
                )
            """)

    # EVENT HANDLER

    def handle_event(self, event):

        if not self.enabled:
            return

        try:
            payload_json = json.dumps(event.payload)
        except Exception:
            payload_json = "{}"

        with self.lock:
            try:
                self.conn.execute(
                    "INSERT INTO events (ts, source, type, payload) VALUES (?, ?, ?, ?)",
                    (
                        event.timestamp,
                        event.source,
                        event.type,
                        payload_json
                    )
                )
                self.conn.commit()

            except Exception as e:
                print(f"SQLiteSink error: {e}")

# This is the End Of File - /services/sqlite_sink.py