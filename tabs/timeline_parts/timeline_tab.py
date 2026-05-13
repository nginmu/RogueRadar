# This is /tabs/timeline_parts/timeline_tab.py
# RR V3 iteration 001
#
# Written by ChatGPT & Claude
# Steered by Nginmu Mbetse
# May 9 2026

import tkinter as tk
from tkinter import ttk

from tabs.timeline_parts.timeline_canvas import TimelineCanvas

class TimelineTab:

    def __init__(self, parent, controller):

        self.controller = controller

        self.frame = ttk.Frame(parent)

        # TOP BAR
        top = ttk.Frame(self.frame)

        top.pack(
            side="top",
            fill="x",
            padx=6,
            pady=6
        )

        title = ttk.Label(
            top,
            text="Temporal rendering engine"
        )

        title.pack(
            side="left"
        )

        # MAIN AREA
        canvas_frame = ttk.Frame(self.frame)

        canvas_frame.pack(
            fill="both",
            expand=True,
            padx=6,
            pady=(0, 6)
        )

        # GRID LAYOUT
        canvas_frame.rowconfigure(0, weight=1)
        canvas_frame.columnconfigure(0, weight=1)

        # TIMELINE CANVAS
        self.timeline = TimelineCanvas(
            canvas_frame
        )

        self.timeline.grid(
            row=0,
            column=0,
            sticky="nsew"
        )

        # HORIZONTAL SCROLLBAR
        x_scroll = ttk.Scrollbar(
            canvas_frame,
            orient="horizontal",
            command=self.timeline.xview
        )

        x_scroll.grid(
            row=1,
            column=0,
            sticky="ew"
        )

        # VERTICAL SCROLLBAR
        y_scroll = ttk.Scrollbar(
            canvas_frame,
            orient="vertical",
            command=self.timeline.yview
        )

        y_scroll.grid(
            row=0,
            column=1,
            sticky="ns"
        )

        self.timeline.configure(
            xscrollcommand=x_scroll.set,
            yscrollcommand=y_scroll.set
        )

    def get_frame(self):

        return self.frame

# This is the End Of File - /tabs/timeline_parts/timeline_tab.py