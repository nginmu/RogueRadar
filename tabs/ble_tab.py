# This is /tabs/ble_tab.py
# RR V3 iteration 001
#
# Written by ChatGPT & Claude
# Steered by Nginmu Mbetse
# May 7 2026

from tabs.base_device_tab import DeviceTableTab

class BLETab(DeviceTableTab):

    def __init__(self, parent, controller):

        columns = ("mac", "rssi", "name", "first", "last")
        column_titles = {
            "mac": "MAC",
            "rssi": "RSSI",
            "name": "Name",
            "first": "First Seen",
            "last": "Last Seen",
        }

        super().__init__(parent, controller, columns, column_titles)

    def _configure_columns(self):
        self.tree.column("mac", width=150)
        self.tree.column("rssi", width=60)
        self.tree.column("name", width=150)
        self.tree.column("first", width=120)
        self.tree.column("last", width=120)

    def extract_values(self, data):
        return (
            data.get("mac"),
            data.get("rssi", ""),
            data.get("name", ""),
            self._format_time(data.get("first_seen")),
            self._format_time(data.get("last_seen")),
        )

# This is the End Of File - /tabs/ble_tab.py