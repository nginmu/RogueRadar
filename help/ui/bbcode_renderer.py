# ============================================================
# Rogue Radar V3
# Chronicles BBCode Renderer
#
# Author:
#     OpenAI ChatGPT
#
# ============================================================

import re


class BBCodeRenderer:

    def __init__(self, text_widget):

        self.text = text_widget

        self.setup_tags()

    # ========================================================
    # TAG CONFIGURATION
    # ========================================================

    def setup_tags(self):

        # ----------------------------------------------------
        # Title
        # ----------------------------------------------------

        self.text.tag_configure(
            "title",
            font=("Consolas", 22, "bold"),
            foreground="#66d9ef",
            spacing3=20
        )

        # ----------------------------------------------------
        # Section headers
        # ----------------------------------------------------

        self.text.tag_configure(
            "section",
            font=("Consolas", 15, "bold"),
            foreground="#8be9fd",
            spacing1=15,
            spacing3=10
        )

        # ----------------------------------------------------
        # Normal body text
        # ----------------------------------------------------

        self.text.tag_configure(
            "body",
            foreground="#dddddd",
            font=("Consolas", 11),
            spacing3=8
        )

        # ----------------------------------------------------
        # Dialogue styles
        # ----------------------------------------------------

        self.create_dialogue_style(
            "nginmu",
            background="#203040",
            accent="#5dade2"
        )

        self.create_dialogue_style(
            "chatgpt",
            background="#203020",
            accent="#50fa7b"
        )

        self.create_dialogue_style(
            "claude",
            background="#302820",
            accent="#ffb86c"
        )

        # ----------------------------------------------------
        # Code blocks
        # ----------------------------------------------------

        self.text.tag_configure(
            "code",
            background="#111111",
            foreground="#50fa7b",
            font=("Consolas", 10),
            lmargin1=30,
            lmargin2=30,
            spacing1=10,
            spacing3=10
        )

        # ----------------------------------------------------
        # Warning blocks
        # ----------------------------------------------------

        self.text.tag_configure(
            "warning",
            background="#402020",
            foreground="#ff6666",
            lmargin1=20,
            lmargin2=20,
            spacing1=10,
            spacing3=10
        )

        # ----------------------------------------------------
        # Tip blocks
        # ----------------------------------------------------

        self.text.tag_configure(
            "tip",
            background="#203020",
            foreground="#88ff88",
            lmargin1=20,
            lmargin2=20,
            spacing1=10,
            spacing3=10
        )

    # ========================================================
    # DIALOGUE STYLE CREATOR
    # ========================================================

    def create_dialogue_style(self, tag, background, accent):

        self.text.tag_configure(
            tag,
            background=background,
            foreground="#dddddd",
            lmargin1=20,
            lmargin2=20,
            spacing1=10,
            spacing3=15
        )

        self.text.tag_configure(
            f"{tag}_speaker",
            foreground=accent,
            font=("Consolas", 11, "bold")
        )

    # ========================================================
    # DOCUMENT LOADING
    # ========================================================

    def load_file(self, path):

        with open(path, "r", encoding="utf-8") as f:

            content = f.read()

        self.render(content)

    # ========================================================
    # MAIN RENDER
    # ========================================================

    def render(self, content):

        self.text.config(state="normal")

        self.text.delete("1.0", "end")

        self.parse(content)

        self.text.config(state="disabled")

    # ========================================================
    # PARSER
    # ========================================================

    def parse(self, content):

        patterns = [

            ("title", r"\[title\](.*?)\[/title\]"),

            ("section", r"\[section\](.*?)\[/section\]"),

            ("nginmu", r"\[nginmu\](.*?)\[/nginmu\]"),

            ("chatgpt", r"\[chatgpt\](.*?)\[/chatgpt\]"),

            ("claude", r"\[claude\](.*?)\[/claude\]"),

            ("warning", r"\[warning\](.*?)\[/warning\]"),

            ("tip", r"\[tip\](.*?)\[/tip\]"),

            ("code", r"\[code(?:=.*?)?\](.*?)\[/code\]"),

        ]

        combined = "|".join(
            f"(?P<{name}>{pattern})"
            for name, pattern in patterns
        )

        position = 0

        for match in re.finditer(combined, content, re.DOTALL):

            start, end = match.span()

            # ------------------------------------------------
            # Plain text between tags
            # ------------------------------------------------

            if start > position:

                plain = content[position:start].strip()

                if plain:

                    self.text.insert(
                        "end",
                        plain + "\n\n",
                        ("body",)
                    )

            tag = match.lastgroup

            full = match.group(tag)

            inner = re.sub(
                r"^\[.*?\]|\[\/.*?\]$",
                "",
                full,
                flags=re.DOTALL
            ).strip()

            self.render_tag(tag, inner)

            position = end

        # ----------------------------------------------------
        # Remaining plain text
        # ----------------------------------------------------

        if position < len(content):

            remain = content[position:].strip()

            if remain:

                self.text.insert(
                    "end",
                    remain,
                    ("body",)
                )

    # ========================================================
    # TAG RENDERER
    # ========================================================

    def render_tag(self, tag, content):

        # ----------------------------------------------------
        # Titles / Sections
        # ----------------------------------------------------

        if tag in ("title", "section"):

            self.text.insert(
                "end",
                content + "\n\n",
                (tag,)
            )

        # ----------------------------------------------------
        # Dialogue blocks
        # ----------------------------------------------------

        elif tag in ("nginmu", "chatgpt", "claude"):

            speaker = tag.capitalize()

            self.text.insert(
                "end",
                speaker + "\n",
                (f"{tag}_speaker", tag)
            )

            self.text.insert(
                "end",
                content + "\n\n",
                (tag,)
            )

        # ----------------------------------------------------
        # Code block
        # ----------------------------------------------------

        elif tag == "code":

            self.text.insert(
                "end",
                content + "\n\n",
                ("code",)
            )

        # ----------------------------------------------------
        # Warning block
        # ----------------------------------------------------

        elif tag == "warning":

            self.text.insert(
                "end",
                "WARNING\n",
                ("warning",)
            )

            self.text.insert(
                "end",
                content + "\n\n",
                ("warning",)
            )

        # ----------------------------------------------------
        # Tip block
        # ----------------------------------------------------

        elif tag == "tip":

            self.text.insert(
                "end",
                "TIP\n",
                ("tip",)
            )

            self.text.insert(
                "end",
                content + "\n\n",
                ("tip",)
            )