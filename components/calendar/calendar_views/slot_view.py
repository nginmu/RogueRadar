# This is /components/calendar/calendar_views/slot_view.py
# RR V3 iteration 001
#
# Written by ChatGPT & Claude
# Steered by Nginmu Mbetse
# May 7 2026

import tkinter as tk

def draw_slot(widget):

    h = widget.current_slot_hour
    m = widget.current_slot_minute
    d = widget.current_date

    end_h = h + (m + 14) // 60
    end_m = (m + 14) % 60

    widget.header.config(
        text=(
            f"{d.strftime('%d %b %Y')}  —  "
            f"{h:02d}:{m:02d} – "
            f"{end_h:02d}:{end_m:02d}"
        )
    )

    CELL_W = 10
    CELL_H = 32
    LABEL_W = 170
    HDR_H = 28
    TOTAL_S = 900

    frame = tk.Frame(widget.container)

    frame.pack(
        fill="both",
        expand=True,
        padx=6,
        pady=6
    )

    hbar = tk.Scrollbar(
        frame,
        orient="horizontal"
    )

    vbar = tk.Scrollbar(
        frame,
        orient="vertical"
    )

    hbar.pack(side="bottom", fill="x")
    vbar.pack(side="right", fill="y")

    canvas = tk.Canvas(
        frame,
        bg="#f5f5f5",
        highlightthickness=1,
        highlightbackground="#aaa",
        xscrollcommand=hbar.set,
        yscrollcommand=vbar.set
    )

    canvas.pack(
        side="left",
        fill="both",
        expand=True
    )

    hbar.config(command=canvas.xview)
    vbar.config(command=canvas.yview)

    canvas_w = LABEL_W + TOTAL_S * CELL_W + 2
    canvas_h = HDR_H + len(widget.tracks) * (CELL_H + 4) + 8

    canvas.config(
        scrollregion=(
            0,
            0,
            canvas_w,
            max(canvas_h, 200)
        )
    )

    # Header
    canvas.create_rectangle(
        0,
        0,
        LABEL_W,
        HDR_H,
        fill="#e0e0e0",
        outline="#ccc"
    )

    canvas.create_text(
        LABEL_W // 2,
        HDR_H // 2,
        text="MAC Track",
        font=("Arial", 8, "bold"),
        fill="#555"
    )

    # Time scale
    for s in range(TOTAL_S):

        rel_min = s // 60
        rel_sec = s % 60
        abs_min = (m + rel_min) % 60
        abs_hour = h + (m + rel_min) // 60
        x = LABEL_W + s * CELL_W

        if rel_sec == 0:

            canvas.create_rectangle(
                x,
                0,
                x + 60 * CELL_W,
                HDR_H,
                fill="#e8e8e8",
                outline="#ccc"
            )

            canvas.create_text(
                x + 4,
                HDR_H // 2,
                text=f"{abs_hour:02d}:{abs_min:02d}",
                anchor="w",
                font=("Arial", 8, "bold"),
                fill="#333"
            )

    # Empty state
    if not widget.tracks:

        canvas.create_text(
            canvas_w // 2,
            80,
            text="No historical events found",
            font=("Arial", 12),
            fill="#888"
        )

        return

    # Tracks
    for ti, track in enumerate(widget.tracks):

        y_top = HDR_H + ti * (CELL_H + 4) + 4
        y_bot = y_top + CELL_H

        canvas.create_rectangle(
            0,
            y_top,
            LABEL_W,
            y_bot,
            fill="#dde8f5",
            outline="#b0c8e8"
        )

        canvas.create_rectangle(
            5,
            y_top + 5,
            14,
            y_bot - 5,
            fill=track.colour,
            outline=""
        )

        canvas.create_text(
            LABEL_W // 2 + 8,
            (y_top + y_bot) // 2,
            text=track.label,
            font=("Arial", 9, "bold"),
            fill="#1a1a2e"
        )

        for s in range(TOTAL_S):

            rel_min = s // 60
            rel_sec = s % 60
            abs_min = (m + rel_min) % 60
            abs_hour = h + (m + rel_min) // 60
            x0 = LABEL_W + s * CELL_W
            x1 = x0 + CELL_W

            has = track.has_event(
                d,
                abs_hour,
                abs_min,
                rel_sec
            )

            fill = (
                track.colour
                if has
                else "white"
            )

            outline = (
                "#bbb"
                if rel_sec == 0
                else "#e8e8e8"
            )

            canvas.create_rectangle(
                x0,
                y_top,
                x1,
                y_bot,
                fill=fill,
                outline=outline
            )

# This is the End Of File - /components/calendar/calendar_views/slot_view.py