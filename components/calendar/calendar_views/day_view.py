# This is /components/calendar/calendar_views/day_view.py
# RR V3 iteration 001
#
# Written by ChatGPT & Claude
# Steered by Nginmu Mbetse
# May 7 2026

import tkinter as tk

def draw_day(widget):

    widget.header.config(
        text=widget.current_date.strftime(
            "%A %d %B %Y"
        )
    )

    HOUR_HEIGHT = 60
    LABEL_WIDTH = 60
    HEADER_HEIGHT = 24
    TOTAL_HEIGHT = HOUR_HEIGHT * 24

    widget.container.rowconfigure(0, weight=1)
    widget.container.columnconfigure(0, weight=0)
    widget.container.columnconfigure(1, weight=1)

    # Hour labels
    hour_canvas = tk.Canvas(
        widget.container,
        width=LABEL_WIDTH,
        bg="#f0f0f0",
        highlightthickness=0
    )

    hour_canvas.grid(
        row=0,
        column=0,
        sticky="nsew",
        pady=(HEADER_HEIGHT, 0)
    )

    hour_canvas.config(
        scrollregion=(0, 0, LABEL_WIDTH, TOTAL_HEIGHT)
    )

    for hour in range(24):

        y = hour * HOUR_HEIGHT

        hour_canvas.create_line(
            0,
            y,
            LABEL_WIDTH,
            y,
            fill="#ccc"
        )

        hour_canvas.create_text(
            LABEL_WIDTH - 4,
            y + HOUR_HEIGHT // 2,
            anchor="e",
            text=f"{hour:02d}:00",
            font=("Arial", 9)
        )

    # Right side
    right = tk.Frame(widget.container)

    right.grid(
        row=0,
        column=1,
        sticky="nsew"
    )

    right.rowconfigure(0, weight=0)
    right.rowconfigure(1, weight=1)
    right.columnconfigure(0, weight=1)
    right.columnconfigure(1, weight=0)

    tk.Frame(
        right,
        width=16,
        height=HEADER_HEIGHT,
        bg="#f0f0f0"
    ).grid(
        row=0,
        column=1,
        sticky="nsew"
    )

    # Minute scale
    min_canvas = tk.Canvas(
        right,
        height=HEADER_HEIGHT,
        bg="#f0f0f0",
        highlightthickness=0
    )

    min_canvas.grid(
        row=0,
        column=0,
        sticky="ew"
    )

    # Scrollbar
    vbar = tk.Scrollbar(
        right,
        orient="vertical"
    )

    vbar.grid(
        row=1,
        column=1,
        sticky="ns"
    )

    # Main grid canvas
    grid_canvas = tk.Canvas(
        right,
        bg="white",
        highlightthickness=0,
        yscrollcommand=vbar.set
    )

    grid_canvas.grid(
        row=1,
        column=0,
        sticky="nsew"
    )

    vbar.config(
        command=lambda *args: (
            grid_canvas.yview(*args),
            hour_canvas.yview(*args),
        )
    )

    # Mouse wheel scrolling
    def on_wheel(event):

        delta = int(-1 * (event.delta / 120))

        grid_canvas.yview_scroll(delta, "units")

        hour_canvas.yview_scroll(delta, "units")

    grid_canvas.bind("<MouseWheel>", on_wheel)

    hour_canvas.bind("<MouseWheel>", on_wheel)

    # Minute scale drawing
    def draw_minute_scale(event=None):

        w = min_canvas.winfo_width()

        if w < 2:
            return

        min_canvas.delete("all")

        mw = w / 60

        min_canvas.create_line(
            0,
            HEADER_HEIGHT - 1,
            w,
            HEADER_HEIGHT - 1,
            fill="#bbb"
        )

        for mn in range(60):

            x = mn * mw

            if mn % 15 == 0:

                tick_h = 10

                min_canvas.create_text(
                    x + 2,
                    HEADER_HEIGHT - tick_h - 2,
                    anchor="sw",
                    text=f":{mn:02d}",
                    font=("Arial", 8),
                    fill="#444"
                )

            elif mn % 5 == 0:

                tick_h = 6

            else:

                tick_h = 3

            min_canvas.create_line(
                x,
                HEADER_HEIGHT - tick_h,
                x,
                HEADER_HEIGHT - 1,
                fill="#aaa"
            )

    min_canvas.bind(
        "<Configure>",
        draw_minute_scale
    )

    # Grid drawing
    def draw_grid(event=None):

        w = grid_canvas.winfo_width()

        if w < 2:
            return

        grid_canvas.delete("all")

        grid_canvas.config(
            scrollregion=(0, 0, w, TOTAL_HEIGHT)
        )

        mw = w / 60

        # Clickable quarter-hour regions
        for hour in range(24):

            y0 = hour * HOUR_HEIGHT
            y1 = y0 + HOUR_HEIGHT

            for slot_m in (0, 15, 30, 45):

                x0 = slot_m * mw
                x1 = (slot_m + 15) * mw

                rid = grid_canvas.create_rectangle(
                    x0,
                    y0,
                    x1,
                    y1,
                    fill="",
                    outline=""
                )

                grid_canvas.tag_bind(
                    rid,
                    "<Enter>",
                    lambda e, r=rid:
                    grid_canvas.itemconfig(
                        r,
                        fill="#ddeeff"
                    )
                )

                grid_canvas.tag_bind(
                    rid,
                    "<Leave>",
                    lambda e, r=rid:
                    grid_canvas.itemconfig(
                        r,
                        fill=""
                    )
                )

                grid_canvas.tag_bind(
                    rid,
                    "<Button-1>",
                    lambda e,
                    hh=hour,
                    sm=slot_m:
                    widget.zoom_slot(hh, sm)
                )

        # Hour boundaries
        for hour in range(24):

            y = hour * HOUR_HEIGHT

            grid_canvas.create_line(
                0,
                y,
                w,
                y,
                fill="#bbb"
            )

            for mn in range(0, 60, 5):

                x = mn * mw

                grid_canvas.create_line(
                    x,
                    y,
                    x,
                    y + 8,
                    fill="#ccc"
                )

        grid_canvas.create_rectangle(
            0,
            0,
            w - 1,
            TOTAL_HEIGHT - 1,
            outline="#aaa"
        )

    grid_canvas.bind(
        "<Configure>",
        draw_grid
    )

# This is the End Of File - /components/calendar/calendar_views/day_view.py