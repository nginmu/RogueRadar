# This is /core/event.py
# RR V3 iteration 001
#
# Written by ChatGPT & Claude
# Steered by Nginmu Mbetse
# May 7 2026

from dataclasses import dataclass, field
from typing import Any, Dict
import time
import uuid

@dataclass(frozen=True)
class Event:
    """
    Canonical event object for Rogue Radar.

    Every piece of data in the system must be converted
    into this format before entering the pipeline.
    """

    # Unique identifier for tracing/debugging
    id: str = field(default_factory=lambda: str(uuid.uuid4()))

    # Event type (e.g. "wifi.packet", "tpms.reading", "system.log")
    type: str = "unknown"

    # Epoch timestamp (float, seconds)
    timestamp: float = field(default_factory=time.time)

    # Source identifier (e.g. "packet_service", "pcap_replay")
    source: str = "unknown"

    # Flexible payload containing event-specific data
    payload: Dict[str, Any] = field(default_factory=dict)

    # Optional metadata (non-essential, debugging, tags, etc.)
    meta: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert Event to dictionary form (for logging, JSON, etc.)
        """
        return {
            "id": self.id,
            "type": self.type,
            "timestamp": self.timestamp,
            "source": self.source,
            "payload": self.payload,
            "meta": self.meta,
        }

# This is the End Of File - /core/event.py