# This is /tabs/timeline_parts/timeline_canvas.py
# RR V3 iteration 001
#
# Written by ChatGPT & Claude
# Steered by Nginmu Mbetse
# May 9 2026

import tkinter as tk
import random

from datetime import datetime

from tabs.timeline_parts.timeline_renderer import draw_timeline

class TimelineCanvas(tk.Canvas):

    def __init__(self, parent):

        super().__init__(
            parent,
            bg="#101010",
            highlightthickness=0
        )

        # LAYOUT

        self.left_margin = 140

        # TEMPORAL STATE

        self.current_time_focus = datetime(
            2021,
            1,
            1,
            0,
            0
        )

        # VIEW STATE

        self.zoom_level = 0

        self.zoom_levels = [

            {
                "name": "Years",
                "segments": 24,
                "width": 5000
            },

            {
                "name": "Months",
                "segments": 12,
                "width": 7000
            },

            {
                "name": "Days",
                "segments": 31,
                "width": 9000
            },

            {
                "name": "Hours",
                "segments": 24,
                "width": 12000
            },

            {
                "name": "Minutes",
                "segments": 60,
                "width": 16000
            }

        ]

        # TRACKS

        self.track_names = [
            "Phone",
            "Router",
            "BLE beacon",
            "TPMS",
            "Unknown cluster",
            "Replay stream",
            "AP mesh",
            "Randomised MAC set",
        ]

        self.track_data = [
            self._generate_fake_activity()
            for _ in self.track_names
        ]

        # INITIAL WIDTH

        self.total_width = (
            self.get_zoom_info()["width"]
        )

        # SCROLLING

        self.configure(
            xscrollincrement=20,
            yscrollincrement=20
        )

        # EVENTS

        self.bind(
            "<Configure>",
            self._on_resize
        )

        self.bind(
            "<Button-1>",
            self._on_left_click
        )

        self.bind(
            "<Button-3>",
            self._on_right_click
        )

        self.draw()

    # FAKE DATA

    def _generate_fake_activity(self):

        values = []

        for i in range(500):

            v = random.random() * 0.05

            if random.random() > 0.94:
                v += random.random()

            if random.random() > 0.985:
                v += 0.7

            values.append(min(v, 1.0))

        return values

    # ZOOM INFO

    def get_zoom_info(self):

        return self.zoom_levels[self.zoom_level]

    # LABELS

    def get_scale_labels(self):

        zoom = self.get_zoom_info()["name"]

        if zoom == "Years":

            start_year = 2000

            return [
                str(start_year + i)
                for i in range(24)
            ]

        elif zoom == "Months":

            return [
                "Jan", "Feb", "Mar", "Apr",
                "May", "Jun", "Jul", "Aug",
                "Sep", "Oct", "Nov", "Dec",
            ]

        elif zoom == "Days":

            return [
                str(i)
                for i in range(1, 32)
            ]

        elif zoom == "Hours":

            return [
                f"{i:02d}:00"
                for i in range(24)
            ]

        elif zoom == "Minutes":

            return [
                f"{i:02d}"
                for i in range(60)
            ]

        return []

    # VIEW DESCRIPTION

    def get_view_description(self):

        focus = self.current_time_focus
        zoom = self.get_zoom_info()["name"]

        if zoom == "Years":

            return "2000–2023"

        elif zoom == "Months":

            return str(focus.year)

        elif zoom == "Days":

            return (
                focus.strftime("%B %Y")
            )

        elif zoom == "Hours":

            return (
                focus.strftime("%d %B %Y")
            )

        elif zoom == "Minutes":

            return (
                focus.strftime(
                    "%d %B %Y %H:00"
                )
            )

        return ""

    # SEGMENT MAPPING

    def get_clicked_segment(self, event):

        zoom = self.get_zoom_info()

        segment_count = zoom["segments"]

        timeline_width = (
            self.total_width
            - self.left_margin
        )

        segment_width = (
            timeline_width / segment_count
        )

        canvas_x = (
            self.canvasx(event.x)
            - self.left_margin
        )

        if canvas_x < 0:
            return None

        segment = int(
            canvas_x / segment_width
        )

        if segment < 0:
            return None

        if segment >= segment_count:
            return None

        return segment

    # TEMPORAL FOCUS UPDATE

    def apply_zoom_focus(self, segment):

        if segment is None:
            return

        zoom_name = (
            self.get_zoom_info()["name"]
        )

        focus = self.current_time_focus

        try:

            if zoom_name == "Years":

                year = 2000 + segment

                self.current_time_focus = (
                    focus.replace(
                        year=year
                    )
                )

            elif zoom_name == "Months":

                month = segment + 1

                self.current_time_focus = (
                    focus.replace(
                        month=month
                    )
                )

            elif zoom_name == "Days":

                day = segment + 1

                self.current_time_focus = (
                    focus.replace(
                        day=day
                    )
                )

            elif zoom_name == "Hours":

                hour = segment

                self.current_time_focus = (
                    focus.replace(
                        hour=hour
                    )
                )

            elif zoom_name == "Minutes":

                minute = segment

                self.current_time_focus = (
                    focus.replace(
                        minute=minute
                    )
                )

        except Exception:
            pass

    # ZOOM CONTROL

    def zoom_in(self):

        if self.zoom_level >= len(self.zoom_levels) - 1:
            return

        old_width = self.total_width

        self.zoom_level += 1

        new_width = (
            self.get_zoom_info()["width"]
        )

        self._preserve_scroll_position(
            old_width,
            new_width
        )

        self.total_width = new_width

        self.draw()

    def zoom_out(self):

        if self.zoom_level <= 0:
            return

        old_width = self.total_width

        self.zoom_level -= 1

        new_width = (
            self.get_zoom_info()["width"]
        )

        self._preserve_scroll_position(
            old_width,
            new_width
        )

        self.total_width = new_width

        self.draw()

    def _preserve_scroll_position(
        self,
        old_width,
        new_width
    ):

        try:

            left_fraction = self.xview()[0]

            old_center = (
                left_fraction * old_width
            )

            new_fraction = (
                old_center / new_width
            )

            self.xview_moveto(new_fraction)

        except Exception:
            pass

    # DRAWING

    def draw(self):

        draw_timeline(self)

    # EVENTS

    def _on_resize(self, event):

        self.draw()

    def _on_left_click(self, event):

        segment = (
            self.get_clicked_segment(event)
        )

        self.apply_zoom_focus(segment)

        self.zoom_in()

    def _on_right_click(self, event):

        self.zoom_out()

# This is the End Of File - /tabs/timeline_parts/timeline_canvas.py