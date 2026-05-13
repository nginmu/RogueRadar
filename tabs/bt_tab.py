# This is /tabs/bt_tab.py
# RR V3 iteration 001
#
# Written by ChatGPT & Claude
# Steered by Nginmu Mbetse
# May 7 2026

from tabs.base_device_tab import DeviceTableTab

class BTTab(DeviceTableTab):

    def __init__(self, parent, controller):
        columns = ("mac", "name", "status")
        column_titles = {
            "mac": "MAC",
            "name": "Name",
            "status": "Status",
        }
        super().__init__(parent, controller, columns, column_titles)

    def _configure_columns(self):
        self.tree.column("mac", width=150)
        self.tree.column("name", width=150)
        self.tree.column("status", width=100)

    def extract_values(self, data):
        return (
            data.get("mac"),
            data.get("name", ""),
            data.get("status", ""),
        )

# This is the End Of File - /tabs/bt_tab.py