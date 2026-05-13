# This is /core/event_bus.py
# RR V3 iteration 001
#
# Written by ChatGPT & Claude
# Steered by Nginmu Mbetse
# May 7 2026

from collections import defaultdict
from typing import Callable, Dict, List
import threading

class EventBus:

    def __init__(self):
        self._subscribers: Dict[str, List[Callable]] = defaultdict(list)
        self._wildcard_subscribers: List[Callable] = []
        self._lock = threading.Lock()

    # SUBSCRIBE

    def subscribe(self, event_type: str, handler: Callable):
        with self._lock:
            if handler not in self._subscribers[event_type]:
                self._subscribers[event_type].append(handler)

    def subscribe_all(self, handler: Callable):
        with self._lock:
            if handler not in self._wildcard_subscribers:
                self._wildcard_subscribers.append(handler)

    # UNSUBSCRIBE

    def unsubscribe(self, event_type: str, handler: Callable):

        with self._lock:
            if handler in self._subscribers.get(event_type, []):
                self._subscribers[event_type].remove(handler)

    def unsubscribe_all(self, handler: Callable):

        with self._lock:
            if handler in self._wildcard_subscribers:
                self._wildcard_subscribers.remove(handler)

    # PUBLISH

    def publish(self, event):

        event_type = getattr(event, "type", None)

        if event_type is None:
            print("EventBus warning: event missing 'type'")
            return

        with self._lock:
            handlers = list(self._subscribers.get(event_type, []))
            wildcard_handlers = list(self._wildcard_subscribers)

        for handler in handlers + wildcard_handlers:
            try:
                handler(event)

            except Exception as e:
                print(f"EventBus handler error: {e}")

# This is the End Of File - /core/event_bus.py