# This is /tabs/timeline_parts/timeline_renderer.py
# RR V3 iteration 001
#
# Written by ChatGPT & Claude
# Steered by Nginmu Mbetse
# May 9 2026

def draw_timeline(canvas):

    canvas.delete("all")

    width = canvas.total_width

    visible_height = max(
        canvas.winfo_height(),
        400
    )

    top_margin = 50
    bottom_margin = 40
    left_margin = 140

    track_count = len(canvas.track_names)

    usable_height = (
        visible_height
        - top_margin
        - bottom_margin
    )

    track_height = max(
        70,
        usable_height // max(track_count, 1)
    )

    total_height = (
        top_margin
        + bottom_margin
        + (track_height * track_count)
    )

    canvas.configure(
        scrollregion=(
            0,
            0,
            width,
            total_height
        )
    )

    # BACKGROUND

    canvas.create_rectangle(
        0,
        0,
        width,
        total_height,
        fill="#101010",
        outline=""
    )

    # ZOOM INFO

    zoom = canvas.get_zoom_info()

    segment_count = zoom["segments"]

    labels = canvas.get_scale_labels()

    zoom_name = zoom["name"]

    view_description = (
        canvas.get_view_description()
    )

    timeline_width = width - left_margin

    segment_width = (
        timeline_width / segment_count
    )

    # HEADER

    canvas.create_text(
        left_margin,
        10,
        anchor="w",
        text=(
            f"Scale: {zoom_name}"
            f"        "
            f"Current view: {view_description}"
        ),
        fill="#b0b0b0",
        font=("Arial", 10, "bold")
    )

    # TOP SCALE BAR

    canvas.create_line(
        left_margin,
        top_margin - 10,
        width,
        top_margin - 10,
        fill="#505050"
    )

    for i in range(segment_count + 1):

        x = left_margin + (
            i * segment_width
        )

        canvas.create_line(
            x,
            top_margin - 18,
            x,
            total_height - bottom_margin,
            fill="#1f1f1f"
        )

        if i < len(labels):

            canvas.create_text(
                x + 4,
                24,
                anchor="nw",
                text=labels[i],
                fill="#909090",
                font=("Arial", 9)
            )

    # TRACKS

    for idx, name in enumerate(
        canvas.track_names
    ):

        y1 = (
            top_margin
            + (idx * track_height)
        )

        y2 = y1 + track_height - 12

        mid_y = (y1 + y2) / 2

        # Track separator

        canvas.create_line(
            left_margin,
            y2 + 6,
            width,
            y2 + 6,
            fill="#242424"
        )

        # Label

        canvas.create_text(
            10,
            mid_y,
            anchor="w",
            text=name,
            fill="#c0c0c0",
            font=("Arial", 10)
        )

        # Background strip

        canvas.create_rectangle(
            left_margin,
            y1,
            width,
            y2,
            fill="#181818",
            outline=""
        )

        # Density bars

        activity = canvas.track_data[idx]

        bar_width = (
            timeline_width / len(activity)
        )

        for i, value in enumerate(activity):

            x1 = (
                left_margin
                + (i * bar_width)
            )

            x2 = x1 + max(bar_width, 1)

            intensity = int(
                40 + (value * 215)
            )

            color = (
                f"#{intensity:02x}"
                f"{intensity:02x}"
                f"{intensity:02x}"
            )

            max_bar_height = (
                (y2 - y1) - 8
            )

            bar_height = (
                value * max_bar_height
            )

            canvas.create_rectangle(
                x1,
                y2 - bar_height,
                x2,
                y2,
                fill=color,
                outline=""
            )

# This is the End Of File - /tabs/timeline_parts/timeline_renderer.py