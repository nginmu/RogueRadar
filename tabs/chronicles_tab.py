# ============================================================
# Rogue Radar V3
# Chronicles Tab
# ============================================================

import tkinter as tk
from tkinter import ttk

from help.ui.bbcode_renderer import BBCodeRenderer


class ChroniclesTab(ttk.Frame):

    def __init__(self, parent, controller=None):

        super().__init__(parent)

        self.controller = controller

        self.build_ui()

    # ========================================================
    # UI
    # ========================================================

    def build_ui(self):

        self.configure(style="Dark.TFrame")

        # ----------------------------------------------------
        # Toolbar
        # ----------------------------------------------------

        toolbar = ttk.Frame(self)

        toolbar.pack(
            fill="x",
            padx=5,
            pady=5
        )

        ttk.Button(
            toolbar,
            text="Index",
            command=lambda: self.load_doc(
                "help/docs/index.bb"
            )
        ).pack(side="left", padx=2)

        # ----------------------------------------------------
        # Text widget
        # ----------------------------------------------------

        self.text = tk.Text(
            self,
            bg="#161616",
            fg="#dddddd",
            insertbackground="white",
            wrap="word",
            relief="flat",
            borderwidth=0,
            padx=20,
            pady=20,
            font=("Consolas", 11)
        )

        scrollbar = ttk.Scrollbar(
            self,
            orient="vertical",
            command=self.text.yview
        )

        self.text.configure(
            yscrollcommand=scrollbar.set
        )

        self.text.pack(
            side="left",
            fill="both",
            expand=True
        )

        scrollbar.pack(
            side="right",
            fill="y"
        )

        # ----------------------------------------------------
        # Renderer
        # ----------------------------------------------------

        self.renderer = BBCodeRenderer(self.text)

        # ----------------------------------------------------
        # Initial document
        # ----------------------------------------------------

        self.load_doc("help/docs/index.bb")

    # ========================================================
    # DOCUMENT LOADING
    # ========================================================

    def load_doc(self, path):

        try:

            self.renderer.load_file(path)

        except Exception as e:

            self.text.config(state="normal")

            self.text.delete("1.0", "end")

            self.text.insert(
                "end",
                f"Failed to load document:\n\n{e}"
            )

            self.text.config(state="disabled")