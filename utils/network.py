# This is /utils/network.py
# RR V3 iteration 001
#
# Written by ChatGPT & Claude
# Steered by Nginmu Mbetse
# May 7 2026

import psutil

def get_network_interfaces(wifi_only=True):

    interfaces = list(psutil.net_if_addrs().keys())

    interfaces = [i for i in interfaces if i != "lo"]

    if wifi_only:
        interfaces = [
            i for i in interfaces
            if i.startswith(("wl", "wlan", "wlp"))
        ]

    return interfaces

# This is the End Of File - /utils/network.py
