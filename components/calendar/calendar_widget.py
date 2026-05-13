# This is /components/calendar/calendar_widget.py
# RR V3 iteration 001
#
# Written by ChatGPT & Claude
# Steered by Nginmu Mbetse
# May 7 2026

from components.calendar.calendar_views.day_view import draw_day
from components.calendar.calendar_views.slot_view import draw_slot
import tkinter as tk
import calendar
from datetime import datetime, timedelta
from services.history_service import HistoryService

class ZoomCalendar(tk.Frame):

    def __init__(self, parent, db_path="events.db"):

        super().__init__(parent, bg="#d0d0d0")

        # Services
        self.history_service = HistoryService(
            db_path=db_path
        )

        # State
        self.current_date = datetime.now()
        self.view_mode = "year"
        self.current_slot_hour = 0
        self.current_slot_minute = 0
        self.tracks = []

        # MAC include filter
        self.included_macs = None

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

        tk.Button(
            nav,
            text="<<",
            command=self.prev
        ).pack(side="left", padx=2)

        tk.Button(
            nav,
            text=">>",
            command=self.next
        ).pack(side="left", padx=2)

        tk.Button(
            nav,
            text="Up",
            command=self.zoom_out
        ).pack(side="left", padx=2)

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

        # Main container
        self.container = tk.Frame(
            self,
            bg="#d0d0d0"
        )

        self.container.pack(
            side="top",
            fill="both",
            expand=True
        )

        # Initial load
        self.reload_tracks()
        self.draw()

    # History loading
    def reload_tracks(self):

        self.tracks = (
            self.history_service.get_tracks_for_day(
                self.current_date,
                included_macs=self.included_macs
            )
        )

    # Utilities
    def clear(self):

        for w in self.container.winfo_children():
            w.destroy()

    def update_breadcrumb(self):

        d = self.current_date
        parts = [str(d.year)]

        if self.view_mode in ("month", "day", "slot"):
            parts.append(
                calendar.month_abbr[d.month]
            )

        if self.view_mode in ("day", "slot"):
            parts.append(str(d.day))

        if self.view_mode == "slot":

            h = self.current_slot_hour
            m = self.current_slot_minute

            end_h = h + (m + 14) // 60
            end_m = (m + 14) % 60

            parts.append(
                f"{h:02d}:{m:02d}"
                f"–"
                f"{end_h:02d}:{end_m:02d}"
            )

        self.breadcrumb.config(
            text="  ›  ".join(parts)
        )

    # Main render dispatch
    def draw(self):

        self.clear()
        self.update_breadcrumb()

        if self.view_mode == "year":
            self.draw_year()

        elif self.view_mode == "month":
            self.draw_month()

        elif self.view_mode == "day":
            self.draw_day()

        elif self.view_mode == "slot":
            self.draw_slot()

    # YEAR VIEW
    def draw_year(self):

        self.header.config(
            text=str(self.current_date.year)
        )

        for i in range(4):
            self.container.columnconfigure(
                i,
                weight=1
            )

        for i in range(3):
            self.container.rowconfigure(
                i,
                weight=1
            )

        for i, month in enumerate(range(1, 13)):

            tk.Button(
                self.container,
                text=calendar.month_abbr[month],
                command=lambda m=month:
                self.zoom_month(m),
            ).grid(
                row=i // 4,
                column=i % 4,
                sticky="nsew",
                padx=5,
                pady=5
            )

    # MONTH VIEW
    def draw_month(self):

        year = self.current_date.year
        month = self.current_date.month

        self.header.config(
            text=f"{calendar.month_name[month]} {year}"
        )

        cal = calendar.monthcalendar(
            year,
            month
        )

        days = [
            "Mon",
            "Tue",
            "Wed",
            "Thu",
            "Fri",
            "Sat",
            "Sun"
        ]

        for i in range(7):
            self.container.columnconfigure(
                i,
                weight=1
            )

        for c, day_name in enumerate(days):

            tk.Label(
                self.container,
                text=day_name,
                bg="#c8c8c8",
                font=("Arial", 9, "bold")
            ).grid(
                row=0,
                column=c,
                sticky="ew",
                padx=2,
                pady=(2, 0)
            )

        for r, week in enumerate(cal):

            for c, day in enumerate(week):

                if day == 0:
                    continue

                tk.Button(
                    self.container,
                    text=str(day),
                    command=lambda d=day:
                    self.zoom_day(d),
                ).grid(
                    row=r + 1,
                    column=c,
                    sticky="nsew",
                    padx=2,
                    pady=2
                )

    # DAY VIEW
    def draw_day(self):
        draw_day(self)

    # SLOT VIEW
    def draw_slot(self):
        draw_slot(self)

    # Navigation
    def zoom_month(self, month):

        self.current_date = self.current_date.replace(
            month=month,
            day=1
        )

        self.reload_tracks()
        self.view_mode = "month"
        self.draw()

    def zoom_day(self, day):

        self.current_date = self.current_date.replace(
            day=day
        )

        self.reload_tracks()
        self.view_mode = "day"
        self.draw()

    def zoom_slot(self, hour, slot_minute):

        self.current_slot_hour = hour
        self.current_slot_minute = slot_minute
        self.view_mode = "slot"
        self.draw()

    def zoom_out(self):

        if self.view_mode == "slot":
            self.view_mode = "day"

        elif self.view_mode == "day":
            self.view_mode = "month"

        elif self.view_mode == "month":
            self.view_mode = "year"

        self.draw()

    def prev(self):

        if self.view_mode == "year":

            self.current_date = self.current_date.replace(
                year=self.current_date.year - 1
            )

        elif self.view_mode == "month":

            mo = self.current_date.month - 1

            if mo == 0:

                self.current_date = self.current_date.replace(
                    year=self.current_date.year - 1,
                    month=12
                )

            else:

                self.current_date = self.current_date.replace(
                    month=mo
                )

        elif self.view_mode == "day":

            self.current_date -= timedelta(days=1)

        elif self.view_mode == "slot":

            mo = self.current_slot_minute - 15
            ho = self.current_slot_hour

            if mo < 0:
                mo = 45
                ho -= 1

            if ho < 0:
                self.current_date -= timedelta(days=1)
                ho = 23
                mo = 45

            self.current_slot_hour = ho
            self.current_slot_minute = mo

        self.reload_tracks()
        self.draw()

    def next(self):

        if self.view_mode == "year":

            self.current_date = self.current_date.replace(
                year=self.current_date.year + 1
            )

        elif self.view_mode == "month":

            mo = self.current_date.month + 1

            if mo == 13:

                self.current_date = self.current_date.replace(
                    year=self.current_date.year + 1,
                    month=1
                )

            else:

                self.current_date = self.current_date.replace(
                    month=mo
                )

        elif self.view_mode == "day":

            self.current_date += timedelta(days=1)

        elif self.view_mode == "slot":

            mo = self.current_slot_minute + 15
            ho = self.current_slot_hour

            if mo >= 60:
                mo = 0
                ho += 1

            if ho >= 24:
                self.current_date += timedelta(days=1)
                ho = 0
                mo = 0

            self.current_slot_hour = ho
            self.current_slot_minute = mo

        self.reload_tracks()
        self.draw()

# This is the End Of File - /components/calendar/calendar_widget.py
