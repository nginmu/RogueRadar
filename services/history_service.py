# This is /services/history_service.py
# RR V3 iteration 001
#
# Written by ChatGPT & Claude
# Steered by Nginmu Mbetse
# May 7 2026

import sqlite3
import json
from datetime import datetime
from components.calendar.track import TimelineTrack

# Track colours

TRACK_COLOURS = [
    "#3a7ebf",
    "#c0392b",
    "#27ae60",
    "#8e44ad",
    "#e67e22",
    "#16a085",
    "#d35400",
    "#2c3e50",
    "#e91e8c",
    "#7f8c8d",
]

class HistoryService:

    def __init__(self, db_path="events.db"):

        self.db_path = db_path

    # DB helpers

    def _connect(self):

        return sqlite3.connect(self.db_path)

    # Public API

    def get_tracks_for_day(
        self,
        date,
        included_macs=None
    ):

        start_ts = datetime(
            date.year,
            date.month,
            date.day,
            0,
            0,
            0
        ).timestamp()

        end_ts = datetime(
            date.year,
            date.month,
            date.day,
            23,
            59,
            59
        ).timestamp()

        conn = self._connect()

        try:

            cur = conn.cursor()

            cur.execute(
                """
                SELECT ts, payload
                FROM events
                WHERE ts >= ?
                AND ts <= ?
                ORDER BY ts ASC
                """,
                (
                    start_ts,
                    end_ts
                )
            )

            rows = cur.fetchall()

        finally:
            conn.close()

        # Build tracks

        tracks = {}

        for ts, payload_json in rows:

            # Decode payload

            try:
                payload = json.loads(payload_json)
            except Exception:
                continue

            mac = payload.get("mac")

            if not mac:
                continue

            # Include filter

            if included_macs is not None:

                if mac not in included_macs:
                    continue

            # Create track if needed

            if mac not in tracks:

                colour = TRACK_COLOURS[
                    len(tracks) % len(TRACK_COLOURS)
                ]

                tracks[mac] = TimelineTrack(
                    track_id=mac,
                    label=mac,
                    colour=colour
                )

            track = tracks[mac]

            # Convert timestamp

            dt = datetime.fromtimestamp(ts)

            # Store event marker

            track.set_event(
                dt,
                dt.hour,
                dt.minute,
                dt.second,
                True
            )

        # Return stable ordered list

        return sorted(
            tracks.values(),
            key=lambda t: t.label
        )


# This is the End Of File - /services/history_service.py
