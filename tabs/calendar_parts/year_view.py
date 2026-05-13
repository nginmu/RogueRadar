# This is /tabs/calendar_parts/year_view.py
# RR V3 iteration 001
#
# Written by ChatGPT & Claude
# Steered by Nginmu Mbetse
# May 7 2026

import tkinter as tk
import calendar

class YearViewMixin:

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
                self.zoom_month(m)
            ).grid(
                row=i // 4,
                column=i % 4,
                sticky="nsew",
                padx=5,
                pady=5
            )

# This is the End Of File - /tabs/calendar_parts/year_view.py