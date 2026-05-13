# This is /core/event_logger.py
# RR V3 iteration 001
#
# Written by ChatGPT & Claude
# Steered by Nginmu Mbetse
# May 7 2026

import json
import threading

class EventLogger:

    def __init__(self, event_bus, filepath="events.log"):
        self.filepath = filepath
        self.enabled = False
        self._lock = threading.Lock()
        event_bus.subscribe_all(self._handle_event)

    # CONTROL

    def enable(self):
        print("EventLogger: ENABLED")
        self.enabled = True

    def disable(self):
        print("EventLogger: DISABLED")
        self.enabled = False

    def toggle(self):
        if self.enabled:
            self.disable()
        else:
            self.enable()

    # EVENT HANDLER

    def _handle_event(self, event):

        if not self.enabled:
            return

        try:
            data = event.to_dict()
            line = json.dumps(data)

            with self._lock:
                with open(self.filepath, "a") as f:
                    f.write(line + "\n")

        except Exception as e:
            print(f"EventLogger error: {e}")

# This is the End Of File - /core/event_logger.py