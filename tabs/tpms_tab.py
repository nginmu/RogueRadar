# This is /tabs/tpms_tab.py
# RR V3 iteration 001
#
# Written by ChatGPT & Claude
# Steered by Nginmu Mbetse
# May 7 2026

from tabs.base_device_tab import DeviceTableTab

class TPMSTab(DeviceTableTab):

    def __init__(self, parent, controller):
        super().__init__(
            parent,
            controller,
            ("id", "pressure", "temperature"),
            {
                "id": "Sensor ID",
                "pressure": "Pressure",
                "temperature": "Temp",
            }
        )

    def get_identifier(self, data):
        return data.get("id")

    def _configure_columns(self):
        self.tree.column("id", width=120)
        self.tree.column("pressure", width=100)
        self.tree.column("temperature", width=100)

    def extract_values(self, data):
        return (
            data.get("id"),
            data.get("pressure", ""),
            data.get("temperature", ""),
        )

# This is the End Of File - /tabs/tpms_tab.py