# This is /tabs/calendar_parts/track.py
# RR V3 iteration 001
#
# Written by ChatGPT & Claude
# Steered by Nginmu Mbetse
# May 7 2026

TRACK_COLOURS = [
    "#3a7ebf", "#c0392b", "#27ae60", "#8e44ad", "#e67e22",
    "#16a085", "#d35400", "#2c3e50", "#e91e8c", "#7f8c8d",
]

class CalendarTrack:

    def __init__(self, name, colour):

        self.name = name
        self.colour = colour
        self.signals = {}

    def signal_key(self, date, abs_hour, abs_min, sec):

        return (
            date.year,
            date.month,
            date.day,
            abs_hour,
            abs_min,
            sec
        )

    def get(self, date, abs_hour, abs_min, sec):

        return self.signals.get(
            self.signal_key(date, abs_hour, abs_min, sec),
            False
        )

    def toggle(self, date, abs_hour, abs_min, sec):

        k = self.signal_key(date, abs_hour, abs_min, sec)

        self.signals[k] = not self.signals.get(k, False)

        return self.signals[k]

# This is the End Of File - /tabs/calendar_parts/track.py