# This is /services/packet_decoder.py
# RR V3 iteration 001
#
# Written by ChatGPT & Claude
# Steered by Nginmu Mbetse
# May 7 2026

from scapy.layers.dot11 import (
    Dot11,
    Dot11Beacon,
    Dot11ProbeResp,
    Dot11ProbeReq
)

# Type / Subtype decoding
def decode_type_subtype(type_, subtype):

    # MANAGEMENT FRAMES
    if type_ == 0:

        mgmt = {
            0: "Association Request",
            1: "Association Response",
            2: "Reassociation Request",
            3: "Reassociation Response",
            4: "Probe Request",
            5: "Probe Response",
            6: "Timing Advertisement",
            7: "Reserved",
            8: "Beacon",
            9: "ATIM",
            10: "Disassociation",
            11: "Authentication",
            12: "Deauthentication",
            13: "Action",
            14: "Action No Ack",
            15: "Reserved",
        }

        return mgmt.get(subtype, f"Mgmt-{subtype}")

    # CONTROL FRAMES
    elif type_ == 1:
        return f"Ctrl-{subtype}"

    # DATA FRAMES
    elif type_ == 2:
        return f"Data-{subtype}"

    # UNKNOWN
    return "Unknown"

# SSID extraction
def extract_ssid(packet):

    try:
        # BEACON FRAMES
        if packet.haslayer(Dot11Beacon):
            ssid = packet[Dot11Beacon].info.decode(errors="ignore")
            return ssid if ssid else "<hidden>"

        # PROBE RESPONSE
        if packet.haslayer(Dot11ProbeResp):
            ssid = packet[Dot11ProbeResp].info.decode(errors="ignore")
            return ssid if ssid else "<hidden>"

        # PROBE REQUEST
        if packet.haslayer(Dot11ProbeReq):
            ssid = packet[Dot11ProbeReq].info.decode(errors="ignore")
            return ssid if ssid else "<hidden>"

    except Exception:
        pass

    # DEFAULT
    return ""

# This is the End Of File - /services/packet_decoder.py