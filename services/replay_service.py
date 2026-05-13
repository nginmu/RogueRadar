# This is /services/replay_service.py
# RR V3 iteration 001
#
# Written by ChatGPT & Claude
# Steered by Nginmu Mbetse
# May 7 2026

import json
import threading
import time
from core.event import Event
from services.data_source import DataSource

class ReplayService(DataSource):

    def __init__(self, event_bus):
        self.event_bus = event_bus
        self._thread = None
        self._stop_event = threading.Event()
        self.filepath = None
        self.speed = 1.0

    def start(self, filepath="events.log", speed=1.0):

        if self.is_running():
            return

        self.filepath = filepath
        self.speed = speed
        self._stop_event.clear()

        self._thread = threading.Thread(
            target=self._run,
            daemon=True
        )
        self._thread.start()

    def stop(self):

        if not self.is_running():
            return

        self._stop_event.set()

        if self._thread:
            self._thread.join(timeout=2)

    def is_running(self):
        return self._thread is not None and self._thread.is_alive()

    def _run(self):

        try:
            with open(self.filepath, "r") as f:

                previous_ts = None

                for line in f:

                    if self._stop_event.is_set():
                        break

                    try:
                        data = json.loads(line.strip())
                    except Exception:
                        continue

                    event = Event(
                        id=data.get("id"),
                        type=data.get("type"),
                        timestamp=data.get("timestamp"),
                        source=data.get("source"),
                        payload=data.get("payload", {}),
                        meta=data.get("meta", {}),
                    )

                    current_ts = event.timestamp

                    if previous_ts is not None:
                        delta = (current_ts - previous_ts) / self.speed
                        if delta > 0:
                            self._stop_event.wait(delta)  # interruptible sleep

                    previous_ts = current_ts

                    self.event_bus.publish(event)

        except Exception as e:
            print(f"Replay error: {e}")

        finally:
            print("Replay finished")

# This is the End Of File - /services/replay_service.py