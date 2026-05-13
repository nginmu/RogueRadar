# This is /gui_window.py
# RR V3 iteration 001
#
# Written by ChatGPT & Claude
# Steered by Nginmu Mbetse
# May 9 2026

import tkinter as tk
from tkinter import ttk

from tabs.main_tab import MainTab
from tabs.chronicles_tab import ChroniclesTab
from tabs.packet_tab import PacketTab
from tabs.bt_tab import BTTab
from tabs.ble_tab import BLETab
from tabs.tpms_tab import TPMSTab
from tabs.ant_tab import ANTTab

from components.calendar import ZoomCalendar
from tabs.timeline_parts.timeline_tab import TimelineTab

import config
from theme import Theme
import os

class AppWindow:

    def __init__(self, controller, model):

        self.controller = controller
        self.model = model

        self.root = tk.Tk()

        icon_path = os.path.join(
            "assets",
            "icon.png"
        )

        self.root.iconphoto(
            True,
            tk.PhotoImage(file=icon_path)
        )

        self.root.title(
            config.WINDOW_TITLE
        )

        self.root.geometry(
            config.WINDOW_SIZE
        )

        self.root.configure(
            bg=Theme.COLOR_BG
        )

        # SAFE SHUTDOWN
        self.root.protocol(
            "WM_DELETE_WINDOW",
            self._on_close
        )

        self._create_tabs()

        self.model.register_observer(
            self
        )

    # TAB SETUP
    def _create_tabs(self):

        self.notebook = ttk.Notebook(
            self.root
        )

        self.notebook.pack(
            expand=True,
            fill="both"
        )

        # CONTROL TABS
        self.main_tab = MainTab(
            self.notebook,
            self.controller
        )

        self.chronicles_tab = ChroniclesTab(
            self.notebook,
            self.controller
        )

        # PROTOCOL TABS
        self.wifi_tab = PacketTab(
            self.notebook,
            self.controller
        )

        self.bt_tab = BTTab(
            self.notebook,
            self.controller
        )

        self.ble_tab = BLETab(
            self.notebook,
            self.controller
        )

        self.tpms_tab = TPMSTab(
            self.notebook,
            self.controller
        )

        self.ant_tab = ANTTab(
            self.notebook,
            self.controller
        )

        # NEW TIMELINE TAB
        self.timeline_tab = TimelineTab(
            self.notebook,
            self.controller
        )

        # OLD CALENDAR PROTOTYPE
        self.calendar_tab = ZoomCalendar(
            self.notebook
        )

        # ADD TABS
        self.notebook.add(
            self.main_tab.get_frame(),
            text=config.TAB_NAMES[0]
        )

        self.notebook.add(
            self.chronicles_tab,
            text=config.TAB_NAMES[1]
        )

        self.notebook.add(
            self.wifi_tab.get_frame(),
            text=config.TAB_NAMES[2]
        )

        self.notebook.add(
            self.bt_tab.get_frame(),
            text=config.TAB_NAMES[3]
        )

        self.notebook.add(
            self.ble_tab.get_frame(),
            text=config.TAB_NAMES[4]
        )

        self.notebook.add(
            self.tpms_tab.get_frame(),
            text=config.TAB_NAMES[5]
        )

        self.notebook.add(
            self.ant_tab.get_frame(),
            text=config.TAB_NAMES[6]
        )

        # NEW SYSTEM
        self.notebook.add(
            self.timeline_tab.get_frame(),
            text="Timeline"
        )

        # OLD PROTOTYPE
        self.notebook.add(
            self.calendar_tab,
            text="History"
        )

    # OBSERVER
    def update(self, key, value, is_new):

        print("UPDATE:", key)

        # CLEAR EVENTS
        if isinstance(key, tuple) and key[0] == "clear":

            protocol = key[1]

            if protocol in ("wifi", "all"):

                self._safe_call(
                    self.wifi_tab.clear
                )

            if protocol in ("bt", "all"):

                self._safe_call(
                    self.bt_tab.clear
                )

            if protocol in ("ble", "all"):

                self._safe_call(
                    self.ble_tab.clear
                )

            if protocol in ("tpms", "all"):

                self._safe_call(
                    self.tpms_tab.clear
                )

            if protocol in ("ant", "all"):

                self._safe_call(
                    self.ant_tab.clear
                )

            return

        # VALIDATION
        if not isinstance(key, tuple):
            return

        protocol, identifier = key

        if not value:
            return

        # ROUTING
        if protocol == "wifi":

            self._safe_call(
                self.wifi_tab.handle_event,
                value,
                is_new
            )

        elif protocol == "bt":

            self._safe_call(
                self.bt_tab.handle_event,
                value,
                is_new
            )

        elif protocol == "ble":

            self._safe_call(
                self.ble_tab.handle_event,
                value,
                is_new
            )

        elif protocol == "tpms":

            self._safe_call(
                self.tpms_tab.handle_event,
                value,
                is_new
            )

        elif protocol == "ant":

            self._safe_call(
                self.ant_tab.handle_event,
                value,
                is_new
            )

    # SAFE UI CALL
    def _safe_call(self, func, *args):

        def wrapper():

            try:

                func(*args)

            except Exception as e:

                print(
                    f"UI update error: {e}"
                )

        self.root.after(
            0,
            wrapper
        )

    # SAFE SHUTDOWN
    def _on_close(self):

        print(
            "Shutting down safely..."
        )

        try:

            if self.controller.is_running():

                print(
                    "Stopping active data source..."
                )

                self.controller.stop_current_source()

        except Exception as e:

            print(
                f"Shutdown error: {e}"
            )

        self.root.destroy()

    # RUN
    def run(self):

        self.root.mainloop()

# End of file /gui_window.py