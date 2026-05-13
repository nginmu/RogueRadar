# This is /tabs/ant_tab.py
# RR V3 iteration 001
#
# Written by ChatGPT & Claude
# Steered by Nginmu Mbetse
# May 7 2026

from tabs.base_device_tab import DeviceTableTab

class ANTTab(DeviceTableTab):

    def __init__(self, parent, controller):
        columns = ("id", "type", "value")
        column_titles = {
            "id": "Device ID",
            "type": "Type",
            "value": "Value",
        }
        super().__init__(parent, controller, columns, column_titles)

    def get_identifier(self, data):
        return data.get("id")

    def _configure_columns(self):
        for column in ("id", "type", "value"):
            self.tree.column(column, width=120)

    def extract_values(self, data):
        return (
            data.get("id"),
            data.get("type", ""),
            data.get("value", ""),
        )

# This is the End Of File - /tabs/ant_tab.py