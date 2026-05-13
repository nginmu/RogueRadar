# This is /tabs/main_tab.py
# RR V3 iteration 001
#
# Written by ChatGPT & Claude
# Steered by Nginmu Mbetse
# May 7 2026

import tkinter as tk
from tkinter import ttk
from utils.network import get_network_interfaces
from utils.probable_ble_adapter import get_probable_ble_adapter

class MainTab:

    def __init__(self, parent, controller):
        self.controller = controller
        self.frame = ttk.Frame(parent)
        self._build_ui()
        self._update_status()
        self.refresh_ble_adapter()

    #UI
    def _build_ui(self):

        #WIFI
        wifi_frame = ttk.LabelFrame(self.frame, text="WiFi")
        wifi_frame.pack(fill="x", padx=10, pady=5)

        for col, weight in enumerate((1, 0, 0)):
            wifi_frame.columnconfigure(col, weight=weight)

        self.interface_var = tk.StringVar()

        self.interface_dropdown = ttk.Combobox(
            wifi_frame,
            textvariable=self.interface_var,
            state="readonly"
        )
        self.interface_dropdown.grid(row=0, column=0, sticky="ew", padx=5)

        self.refresh_button = ttk.Button(
            wifi_frame,
            text="↻",
            width=3,
            command=self.load_interfaces
        )
        self.refresh_button.grid(row=0, column=1, padx=5)

        self.wifi_button = ttk.Button(
            wifi_frame,
            text="Start WiFi",
            command=self._toggle_wifi
        )
        self.wifi_button.grid(row=0, column=2, padx=5)

        self.load_interfaces()

        #BLE
        ble_frame = ttk.LabelFrame(self.frame, text="BLE")
        ble_frame.pack(fill="x", padx=10, pady=5)

        for col, weight in enumerate((1, 0, 0)):
            ble_frame.columnconfigure(col, weight=weight)

        self.ble_adapter_var = tk.StringVar(value="Detecting...")

        self.ble_adapter_label = ttk.Label(
            ble_frame,
            textvariable=self.ble_adapter_var,
            anchor="w"
        )
        self.ble_adapter_label.grid(row=0, column=0, sticky="ew", padx=5)

        self.ble_refresh_button = ttk.Button(
            ble_frame,
            text="↻",
            width=3,
            command=self.refresh_ble_adapter
        )
        self.ble_refresh_button.grid(row=0, column=1, padx=5)

        self.ble_button = ttk.Button(
            ble_frame,
            text="Start BLE",
            command=self._toggle_ble
        )
        self.ble_button.grid(row=0, column=2, padx=5)

        #SYSTEM
        system_frame = ttk.LabelFrame(self.frame, text="System")
        system_frame.pack(fill="x", padx=10, pady=5)

        self.log_button = ttk.Button(
            system_frame,
            text="Toggle Logging",
            command=self._toggle_logging
        )
        self.log_button.pack(side="left", padx=5)

        self.sqlite_button = ttk.Button(
            system_frame,
            text="Toggle SQLite",
            command=self._toggle_sqlite
        )
        self.sqlite_button.pack(side="left", padx=5)

        #STATUS
        self.status_var = tk.StringVar()

        self.status_label = ttk.Label(
            self.frame,
            textvariable=self.status_var
        )
        self.status_label.pack(anchor="w", padx=10, pady=10)

    #WIFI CONTROL
    def _toggle_wifi(self):

        if self.controller.current_protocol == "wifi":
            self.controller.stop_current_source()
        else:
            interface = self.interface_var.get()
            if not interface:
                print("No interface selected")
                return
            self.controller.start_source("wifi", interface=interface)

        self._update_status()

    #BLE CONTROL
    def _toggle_ble(self):

        if self.controller.current_protocol == "ble":
            self.controller.stop_current_source()
        else:
            self.controller.stop_current_source()
            self.controller.start_source("ble")

        self._update_status()

    #SYSTEM CONTROLS
    def _toggle_logging(self):
        self.controller.toggle_logging()
        self._update_status()

    def _toggle_sqlite(self):
        self.controller.toggle_sqlite()
        self._update_status()

    #BLE ADAPTER
    def refresh_ble_adapter(self):

        try:
            info = get_probable_ble_adapter()

            if not info:
                self.ble_adapter_var.set("Unavailable")
                return

            text = (
                f"{info.get('name', 'Unknown')} "
                f"({info.get('adapter', '?')}) "
                f"(~{int(info.get('confidence', 0) * 100)}%)"
            )

        except Exception as e:
            print(f"BLE adapter error: {e}")
            text = "Unavailable"

        self.ble_adapter_var.set(text)

    #STATUS
    def _update_status(self):

        protocol = self.controller.current_protocol
        wifi_running = protocol == "wifi"
        ble_running = protocol == "ble"

        self.interface_dropdown.config(
            state="disabled" if wifi_running else "readonly"
        )
        self.refresh_button.config(
            state="disabled" if wifi_running else "normal"
        )

        self.wifi_button.config(
            text="Stop WiFi" if wifi_running else "Start WiFi"
        )
        self.ble_button.config(
            text="Stop BLE" if ble_running else "Start BLE"
        )

        logging = "ON" if self.controller.is_logging_enabled() else "OFF"
        sqlite = "ON" if self.controller.is_sqlite_enabled() else "OFF"

        self.status_var.set(
            f"Active: {protocol or 'None'} | "
            f"Logging: {logging} | SQLite: {sqlite}"
        )

    #INTERFACES
    def load_interfaces(self):

        interfaces = get_network_interfaces(wifi_only=True)
        current = self.interface_var.get()

        self.interface_dropdown["values"] = interfaces or []

        if not interfaces:
            self.interface_var.set("")
        elif current in interfaces:
            self.interface_var.set(current)
        else:
            self.interface_dropdown.current(0)

    #FRAME
    def get_frame(self):
        return self.frame

# This is the End Of File - /tabs/main_tab.py