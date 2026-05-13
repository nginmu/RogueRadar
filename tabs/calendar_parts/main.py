# This is /tabs/calendar_parts/main.py
# RR V3 iteration 001
#
# Written by ChatGPT & Claude
# Steered by Nginmu Mbetse
# May 7 2026

import tkinter as tk
from datetime import datetime
from tabs.calendar_parts.helpers import CalendarHelpers
from tabs.calendar_parts.navigation import CalendarNavigation
from tabs.calendar_parts.year_view import YearViewMixin

class ZoomCalendar(
    CalendarHelpers,
    CalendarNavigation,
    YearViewMixin,
    tk.Frame,
):

    def __init__(self, parent):

        super().__init__(parent, bg="#d0d0d0")
        self.current_date = datetime.now()
        self.view_mode = "year"
        self.current_slot_hour = 0
        self.current_slot_minute = 0
        self.tracks = []

        # Top bar
        top = tk.Frame(self, bg="#e8e8e8")

        top.pack(
            side="top",
            fill="x"
        )

        self.header = tk.Label(
            top,
            font=("Arial", 18),
            bg="#e8e8e8"
        )

        self.header.pack(
            side="top",
            pady=8
        )

        nav = tk.Frame(
            top,
            bg="#e8e8e8"
        )

        nav.pack(
            side="top",
            pady=(0, 6)
        )

        for text, cmd in (
            ("<<", self.prev),
            (">>", self.next),
            ("Up", self.zoom_out),
        ):

            tk.Button(
                nav,
                text=text,
                command=cmd
            ).pack(
                side="left",
                padx=2
            )

        self.breadcrumb = tk.Label(
            top,
            font=("Arial", 9),
            bg="#e8e8e8",
            fg="#666"
        )

        self.breadcrumb.pack(
            side="top",
            pady=(0, 4)
        )

        self.container = tk.Frame(
            self,
            bg="#d0d0d0"
        )

        self.container.pack(
            side="top",
            fill="both",
            expand=True
        )

        self.draw()

    def draw_month(self):

        self.header.config(text="Month")

    def draw_day(self):

        self.header.config(text="Day")

    def draw_slot(self):

        self.header.config(text="Slot")

# This is the End Of File - /tabs/calendar_parts/main.py