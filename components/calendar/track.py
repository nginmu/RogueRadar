# This is /components/calendar/track.py
# RR V3 iteration 001
#
# Written by ChatGPT & Claude
# Steered by Nginmu Mbetse
# May 7 2026

class TimelineTrack:

    def __init__(
        self,
        track_id,
        label=None,
        colour="#3a7ebf"
    ):

        self.id = track_id
        self.label = label or track_id
        self.colour = colour
        self.events = {}

    # Internal helpers
    def _key(
        self,
        date,
        abs_hour,
        abs_minute,
        second
    ):

        return (
            date.year,
            date.month,
            date.day,
            abs_hour,
            abs_minute,
            second
        )

    # Public API

    def has_event(
        self,
        date,
        abs_hour,
        abs_minute,
        second
    ):

        return self.events.get(
            self._key(
                date,
                abs_hour,
                abs_minute,
                second
            ),
            False
        )

    def set_event(
        self,
        date,
        abs_hour,
        abs_minute,
        second,
        present=True
    ):

        self.events[
            self._key(
                date,
                abs_hour,
                abs_minute,
                second
            )
        ] = present

# This is the End Of File - /components/calendar/track.py
