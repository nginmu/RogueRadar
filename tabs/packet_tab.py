# This is /tabs/packet_tab.py
# RR V3 iteration 001
#
# Written by ChatGPT & Claude
# Steered by Nginmu Mbetse
# May 7 2026

from tabs.base_device_tab import DeviceTableTab
from services.packet_descriptions import get_description

class PacketTab(DeviceTableTab):

    def __init__(self, parent, controller):

        columns = ("mac", "rssi", "role", "type", "ssid", "count", "first", "last")

        super().__init__(
            parent,
            controller,
            columns,
            {
                "mac": "MAC",
                "rssi": "RSSI",
                "role": "Role",
                "type": "Type",
                "ssid": "SSID",
                "count": "Count",
                "first": "First Seen",
                "last": "Last Seen",
            }
        )

    def _configure_columns(self):
        for column, width in {
            "mac": 150,
            "rssi": 60,
            "role": 80,
            "type": 120,
            "ssid": 150,
            "count": 60,
            "first": 120,
            "last": 120,
        }.items():
            self.tree.column(column, width=width)

    def extract_values(self, data):
        return (
            data.get("mac"),
            data.get("rssi", "") if data.get("rssi") is not None else "",
            data.get("role", "Other"),
            data.get("type", "?"),
            data.get("ssid", ""),
            data.get("packet_count", 0),
            self._format_time(data.get("first_seen")),
            self._format_time(data.get("last_seen")),
        )

    def get_tooltip_text(self, data, column):
        if column != "type":
            return None

        pkt_type = data.get("type", "")
        return get_description(pkt_type) if pkt_type else None

# This is the End Of File - /tabs/packet_tab.py