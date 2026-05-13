# This is /utils/probable_ble_adapter.py
# RR V3 iteration 001
#
# Written by ChatGPT & Claude
# Steered by Nginmu Mbetse
# May 7 2026

import subprocess
import re
import os
import config

# COMMAND HELPER

def _run(cmd):
    try:
        result = subprocess.run(
            cmd,
            shell=True,
            capture_output=True,
            text=True
        )
        return result.stdout.strip()
    except Exception:
        return ""

# BASIC DETECTION

def _get_hci():
    out = _run("hciconfig")
    match = re.search(r"(hci\d+):", out)
    return match.group(1) if match else None

def _get_mac(hci):
    out = _run(f"hciconfig {hci}")
    match = re.search(r"BD Address: ([0-9A-F:]+)", out)
    return match.group(1) if match else None

# SYSFS (BEST SOURCE)

def _get_sysfs_info(hci):
    base = f"/sys/class/bluetooth/{hci}/device"

    vendor = ""
    device = ""

    try:
        if os.path.exists(base):

            vendor_path = os.path.join(base, "manufacturer")
            product_path = os.path.join(base, "product")

            if os.path.exists(vendor_path):
                with open(vendor_path) as f:
                    vendor = f.read().strip()

            if os.path.exists(product_path):
                with open(product_path) as f:
                    device = f.read().strip()

    except Exception:
        pass

    return vendor, device

# LSUSB FALLBACK

def _get_lsusb_match():
    out = _run("lsusb")

    for line in out.splitlines():
        if "Bluetooth" in line:
            return line

    return ""

# OUI LOOKUP

_oui_cache = None

def _load_oui_map():
    global _oui_cache

    if _oui_cache is not None:
        return _oui_cache

    utils_dir = os.path.dirname(os.path.abspath(__file__))
    filepath = os.path.join(utils_dir, config.OUI_FILE)
    oui_map = {}

    try:
        with open(filepath, "r", errors="ignore") as f:
            for line in f:

                # Match lines like:
                # 08-EA-44   (hex)   Vendor Name
                match = re.match(r"^([0-9A-Fa-f\-]{8})\s+\(hex\)\s+(.+)", line)

                if match:
                    prefix = match.group(1).replace("-", ":").upper()
                    vendor = match.group(2).strip()
                    oui_map[prefix] = vendor

    except Exception:
        pass

    _oui_cache = oui_map
    return oui_map

def _lookup_vendor_from_mac(mac):
    if not mac:
        return None

    oui_map = _load_oui_map()
    prefix = mac.upper()[0:8]  # AA:BB:CC
    return oui_map.get(prefix)

# MAIN FUNCTION

def get_probable_ble_adapter():

    hci = _get_hci()

    if not hci:
        return {
            "adapter": None,
            "name": "No adapter found",
            "mac": None,
            "confidence": 0.0
        }

    mac = _get_mac(hci)
    vendor, device = _get_sysfs_info(hci)
    name = ""
    confidence = 0.3

    # BEST: SYSFS
    if vendor or device:
        name = f"{vendor} {device}".strip()
        confidence = 0.9

    # OUI LOOKUP
    if not name and mac:
        vendor_from_mac = _lookup_vendor_from_mac(mac)

        if vendor_from_mac:
            name = f"{vendor_from_mac} (via MAC)"
            confidence = 0.85

    # LSUSB
    if not name:
        usb_line = _get_lsusb_match()

        if usb_line:
            name = usb_line.split("ID")[-1].strip()
            confidence = 0.7

    # FINAL FALLBACK
    if not name:
        name = "Unknown adapter"
        confidence = 0.4

    return {
        "adapter": hci,
        "name": name,
        "mac": mac,
        "confidence": round(confidence, 2)
    }

# This is the End Of File - /utils/probable_ble_adapter.py