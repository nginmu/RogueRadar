# This is /tabs/calendar_parts/navigation.py
# RR V3 iteration 001
#
# Written by ChatGPT & Claude
# Steered by Nginmu Mbetse
# May 7 2026

from datetime import timedelta

class CalendarNavigation:

    def zoom_month(self, month):

        self.current_date = self.current_date.replace(
            month=month,
            day=1
        )

        self.view_mode = "month"
        self.draw()

    def zoom_day(self, day):

        self.current_date = self.current_date.replace(
            day=day
        )

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

            self.current_date = (
                self.current_date.replace(
                    year=self.current_date.year - 1,
                    month=12
                )
                if mo == 0
                else self.current_date.replace(month=mo)
            )

        elif self.view_mode == "day":

            self.current_date -= timedelta(days=1)

        elif self.view_mode == "slot":

            mo = self.current_slot_minute - 15
            ho = self.current_slot_hour

            if mo < 0:
                mo, ho = 45, ho - 1

            if ho < 0:

                self.current_date -= timedelta(days=1)
                ho, mo = 23, 45

            self.current_slot_hour = ho
            self.current_slot_minute = mo

        self.draw()

    def next(self):

        if self.view_mode == "year":

            self.current_date = self.current_date.replace(
                year=self.current_date.year + 1
            )

        elif self.view_mode == "month":

            mo = self.current_date.month + 1

            self.current_date = (
                self.current_date.replace(
                    year=self.current_date.year + 1,
                    month=1
                )
                if mo == 13
                else self.current_date.replace(month=mo)
            )

        elif self.view_mode == "day":

            self.current_date += timedelta(days=1)

        elif self.view_mode == "slot":

            mo = self.current_slot_minute + 15
            ho = self.current_slot_hour

            if mo >= 60:
                mo, ho = 0, ho + 1

            if ho >= 24:

                self.current_date += timedelta(days=1)
                ho, mo = 0, 0

            self.current_slot_hour = ho
            self.current_slot_minute = mo

        self.draw()

# This is the End Of File - /tabs/calendar_parts/navigation.py