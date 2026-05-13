# This is /tabs/base_device_tab.py
# RR V3 iteration 001
#
# Written by ChatGPT & Claude
# Steered by Nginmu Mbetse
# May 7 2026

import tkinter as tk
from tkinter import ttk
from datetime import datetime
from components.tooltip import ToolTip

class DeviceTableTab:

    def __init__(self, parent, controller, columns, column_titles):
        self.controller = controller
        self.frame = ttk.Frame(parent)

        self.columns = columns
        self.column_titles = column_titles

        tree_frame = ttk.Frame(self.frame)
        tree_frame.pack(fill="both", expand=True)

        self.tree = ttk.Treeview(tree_frame, columns=self.columns, show="headings")

        scrollbar = ttk.Scrollbar(
            tree_frame,
            orient="vertical",
            command=self.tree.yview
        )

        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        for col in self.columns:
            self.tree.heading(
                col,
                text=self.column_titles[col],
                command=lambda c=col: self._on_heading_click(c)
            )

        self._configure_columns()

        self.rows = {}
        self.sort_column = None
        self.sort_reverse = False

        self.tooltip = ToolTip(self.tree)

        self.tree.bind("<Motion>", self._on_mouse_motion)
        self.tree.bind("<Leave>", self._on_mouse_leave)

        self.menu = tk.Menu(self.frame, tearoff=0)
        self.menu.add_command(label="Ignore device", command=self._ignore_selected)

        self.tree.bind("<Button-3>", self._show_context_menu)
        self.tree.bind("<Button-2>", self._show_context_menu)

    # OVERRIDES
    def _configure_columns(self):
        pass

    def extract_values(self, data):
        raise NotImplementedError

    def get_tooltip_text(self, data, column):
        """Return tooltip text for a hovered row/column, or None."""
        return None

    # TOOLTIP HANDLERS
    def _on_mouse_motion(self, event):
        if self.tree.identify("region", event.x, event.y) != "cell":
            self.tooltip.hide()
            return

        row_id = self.tree.identify_row(event.y)
        col_id = self.tree.identify_column(event.x)

        if not row_id or not col_id:
            self.tooltip.hide()
            return

        try:
            column = self.columns[int(col_id.replace("#", "")) - 1]
            values = self.tree.item(row_id, "values")
            identifier = values[0]
        except Exception:
            self.tooltip.hide()
            return

        if not values:
            self.tooltip.hide()
            return

        data = self._get_data_for_identifier(identifier)

        if not data:
            self.tooltip.hide()
            return

        text = self.get_tooltip_text(data, column)

        if text:
            self.tooltip.show(
                text,
                self.tree.winfo_rootx() + event.x + 20,
                self.tree.winfo_rooty() + event.y + 10
            )
        else:
            self.tooltip.hide()

    def _on_mouse_leave(self, event):
        self.tooltip.hide()

    def _get_data_for_identifier(self, identifier):
        """Look up live model data for a given identifier."""
        try:
            protocol = self.controller.current_protocol
            if protocol:
                return self.controller.model.get_devices(protocol).get(identifier)
        except Exception:
            pass
        return None

    # TIME
    def _format_time(self, ts):
        try:
            return datetime.fromtimestamp(ts).strftime("%H:%M:%S")
        except Exception:
            return ""

    # SORT
    def _on_heading_click(self, col):
        """
        Handle a column heading click.
        col is always the clean column name.
        """
        if self.sort_column == col:
            self.sort_reverse = not self.sort_reverse
        else:
            self.sort_column = col
            self.sort_reverse = False

        self._update_heading_arrows()
        self._apply_sort()

    def _update_heading_arrows(self):
        """Refresh heading text with active sort arrows."""
        for col in self.columns:
            title = self.column_titles[col]

            if col == self.sort_column:
                title += " ▼" if self.sort_reverse else " ▲"

            self.tree.heading(col, text=title)

    def _apply_sort(self):
        if not self.sort_column:
            return

        col_index = self.columns.index(self.sort_column)

        def sort_key(item):
            value = item[1][col_index]
            try:
                return float(value)
            except Exception:
                return str(value).lower()

        data = [
            (row_id, self.tree.item(row_id, "values"))
            for row_id in self.tree.get_children()
        ]

        data.sort(key=sort_key, reverse=self.sort_reverse)

        for index, (row_id, _) in enumerate(data):
            self.tree.move(row_id, "", index)

    # CONTEXT MENU
    def _show_context_menu(self, event):
        row_id = self.tree.identify_row(event.y)

        if not row_id:
            return

        self.tree.selection_set(row_id)
        self.menu.post(event.x_root, event.y_root)

    def _ignore_selected(self):
        selected = self.tree.selection()

        if not selected:
            return

        row_id = selected[0]
        identifier = self.tree.item(row_id, "values")[0]

        try:
            self.controller.model.add_to_ignore(identifier)
            print(f"Ignored: {identifier}")
        except Exception as e:
            print(f"Ignore error: {e}")

    # CORE ENGINE
    def handle_event(self, data, is_new):
        if not data:
            return

        identifier = self.get_identifier(data)

        if not identifier:
            return

        values = self.extract_values(data)

        if identifier in self.rows:
            row_id = self.rows[identifier]

            if row_id not in self.tree.get_children():
                del self.rows[identifier]
            else:
                self.tree.item(row_id, values=values)

        if identifier not in self.rows:
            self.rows[identifier] = self.tree.insert(
                "",
                "end",
                values=values
            )

        if self.sort_column:
            self._apply_sort()

    def get_identifier(self, data):
        return data.get("mac")

    def clear(self):
        for row in self.tree.get_children():
            self.tree.delete(row)

        self.rows.clear()

    def get_frame(self):
        return self.frame

# This is the End Of File - /tabs/base_device_tab.py