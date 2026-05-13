# This is /tabs/calendar_parts/helpers.py
# RR V3 iteration 001
#
# Written by ChatGPT & Claude
# Steered by Nginmu Mbetse
# May 7 2026

import calendar

class CalendarHelpers:

    def clear(self):

        for w in self.container.winfo_children():
            w.destroy()

        for i in range(20):

            self.container.columnconfigure(
                i,
                weight=0,
                minsize=0
            )

            self.container.rowconfigure(
                i,
                weight=0,
                minsize=0
            )

    def update_breadcrumb(self):

        d = self.current_date

        parts = [str(d.year)]

        if self.view_mode in ("month", "day", "slot"):
            parts.append(calendar.month_abbr[d.month])

        if self.view_mode in ("day", "slot"):
            parts.append(str(d.day))

        if self.view_mode == "slot":

            h = self.current_slot_hour
            m = self.current_slot_minute

            end_h = h + (m + 14) // 60
            end_m = (m + 14) % 60

            parts.append(
                f"{h:02d}:{m:02d}–{end_h:02d}:{end_m:02d}"
            )

        self.breadcrumb.config(
            text="  ›  ".join(parts)
        )

    def draw(self):

        self.clear()
        self.update_breadcrumb()

        {
            "year": self.draw_year,
            "month": self.draw_month,
            "day": self.draw_day,
            "slot": self.draw_slot,
        }[self.view_mode]()

# This is the End Of File - /tabs/calendar_parts/helpers.py