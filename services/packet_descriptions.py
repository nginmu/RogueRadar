# This is /services/packet_descriptions.py
# RR V3 iteration 001
#
# Written by ChatGPT & Claude
# Steered by Nginmu Mbetse
# May 7 2026

TYPE_DESCRIPTIONS = {
    "Beacon":                  "AP advertisement: periodically announces an access point and its capabilities.",
    "Probe Response":          "AP reply to a probe: contains SSID and supported rates.",
    "Probe Request":           "Client probe: device searching for networks (may include SSID wildcard).",
    "Association Request":     "Client request to join an AP (starts connection process).",
    "Association Response":    "AP response to association (accept or reject).",
    "Reassociation Request":   "Client roaming: asking a new AP to take over an association.",
    "Reassociation Response":  "AP response to reassociation request.",
    "Authentication":          "Authentication frame: part of the open/shared key auth exchange.",
    "Deauthentication":        "Deauthentication: AP or client terminating authentication.",
    "Disassociation":          "Disassociation: AP or client disconnecting from network.",
    "Action":                  "Action frame: used for control operations (e.g. spectrum mgmt, QoS).",
    "Action No Ack":           "Action frame that does not require acknowledgement.",
    "ATIM":                    "Ad hoc traffic indication: used in IBSS (ad hoc) power-save mode.",
    "Block Ack Req":           "Block Ack Request: part of block acknowledgement aggregation.",
    "Block Ack":               "Block Ack: acknowledgement for aggregated frames.",
    "PS-Poll":                 "Power Save Poll: client asking AP for buffered frames (power-save).",
    "Timing Advertisement":    "Timing Advertisement: used for time synchronisation.",
    "Reserved":                "Reserved frame subtype (not used in standard 802.11).",
    "Other":                   "Other management, control, or data frame.",
}

# FALLBACK POPULATION

# Mgmt-X fallbacks (management subtypes by number)
for _s in range(0, 16):
    _key = f"Mgmt-{_s}"
    if _key not in TYPE_DESCRIPTIONS:
        TYPE_DESCRIPTIONS[_key] = f"Management frame subtype {_s} (802.11)."

# Ctrl-X fallbacks (format produced by packet_decoder.py for control frames)
for _s in range(0, 16):
    _key = f"Ctrl-{_s}"
    if _key not in TYPE_DESCRIPTIONS:
        TYPE_DESCRIPTIONS[_key] = f"Control frame subtype {_s} (e.g. ACK, RTS, CTS, PS-Poll)."

# Data-X fallbacks (format produced by packet_decoder.py for data frames)
for _s in range(0, 16):
    _key = f"Data-{_s}"
    if _key not in TYPE_DESCRIPTIONS:
        TYPE_DESCRIPTIONS[_key] = f"Data frame subtype {_s} (carries network payload or QoS data)."

# LOOKUP FUNCTION
def get_description(pkt_type):
    return TYPE_DESCRIPTIONS.get(pkt_type, "")

# This is the End Of File - /services/packet_descriptions.py
