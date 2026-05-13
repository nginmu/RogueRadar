# This is /services/interface_service.py
# RR V3 iteration 001
#
# Written by ChatGPT & Claude
# Steered by Nginmu Mbetse
# May 7 2026

import subprocess
import shlex

# COMMAND HELPER

def run(cmd):

    try:
        return subprocess.run(
            shlex.split(cmd),
            capture_output=True,
            text=True
        )
    except Exception as e:
        cp = subprocess.CompletedProcess(args=cmd, returncode=1)
        cp.stderr = str(e)
        return cp

# NETWORKMANAGER CONTROL

def nm_stop():
    return run("systemctl stop NetworkManager")

def nm_start():
    return run("systemctl start NetworkManager")

def nm_unmanage(iface):
    return run(f"nmcli device set {shlex.quote(iface)} managed no")

def nm_remanage(iface):
    return run(f"nmcli device set {shlex.quote(iface)} managed yes")

# INTERFACE CONTROL

def iface_down(iface):
    return run(f"ip link set {shlex.quote(iface)} down")

def iface_up(iface):
    return run(f"ip link set {shlex.quote(iface)} up")

# MONITOR MODE SETUP

def add_mon_interface(iface, mon="mon0"):
    return run(f"iw dev {shlex.quote(iface)} interface add {shlex.quote(mon)} type monitor")

def del_mon_interface(mon="mon0"):
    return run(f"iw dev {shlex.quote(mon)} del")

def set_iface_type(iface, mode):
    return run(f"iw dev {shlex.quote(iface)} set type {shlex.quote(mode)}")

# STATE

monitor_created = False      # Did we create a new monitor interface?
current_mon = "mon0"         # Name of monitor interface
current_phy_iface = None     # Original physical interface (e.g. wlan1)

# MAIN FUNCTIONS

def enable_monitor_mode(phy_iface):

    global monitor_created, current_mon, current_phy_iface
    current_phy_iface = phy_iface

    # RELEASE FROM NETWORKMANAGER

    nm_unmanage(phy_iface)

    # PREPARE INTERFACE

    try:
        iface_down(phy_iface)
    except Exception:
        pass

    # TRY CREATING MONITOR INTERFACE

    r = add_mon_interface(phy_iface, current_mon)

    if r.returncode != 0:

        try:
            set_iface_type(phy_iface, "monitor")
            current_mon = phy_iface
            monitor_created = False
            iface_up(current_mon)

        except Exception:
            raise

    else:
        try:
            iface_up(current_mon)
            monitor_created = True

        except Exception:
            raise

    return current_mon

def disable_monitor_mode():

    global monitor_created, current_mon, current_phy_iface

    # BRING DOWN MONITOR INTERFACE

    try:
        iface_down(current_mon)
    except Exception:
        pass

    # REMOVE MONITOR INTERFACE

    if monitor_created:
        try:
            del_mon_interface(current_mon)
        except Exception:
            pass

    # RESTORE ORIGINAL INTERFACE

    try:
        iface_down(current_phy_iface)
        set_iface_type(current_phy_iface, "managed")
        iface_up(current_phy_iface)
    except Exception:
        pass

    # HAND BACK TO NETWORKMANAGER

    try:
        nm_remanage(current_phy_iface)
    except Exception:
        pass

# This is end of file of /services/interface_service.py
