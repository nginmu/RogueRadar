# This is /services/packet_service.py
# RR V3 iteration 001
#
# Written by ChatGPT & Claude
# Steered by Nginmu Mbetse
# May 7 2026

from scapy.all import sniff
from scapy.layers.dot11 import Dot11
import threading
import time
import os
from services.data_source import DataSource

class PacketService(DataSource):

    def __init__(self):
        self._thread = None
        self._hopper_thread = None
        self._stop_event = threading.Event()
        self.on_packet = None

    def start(self, interface):

        if self.is_running():
            return

        self._stop_event.clear()

        # CHANNEL HOPPER

        def hop_channels():
            channels = list(range(1, 14))
            i = 0

            while not self._stop_event.is_set():
                channel = channels[i % len(channels)]
                os.system(
                    f"iw dev {interface} set channel {channel} > /dev/null 2>&1"
                )
                i += 1
                self._stop_event.wait(0.3)  # interruptible sleep

        self._hopper_thread = threading.Thread(
            target=hop_channels,
            daemon=True
        )
        self._hopper_thread.start()

        # PACKET SNIFFER

        def run():
            while not self._stop_event.is_set():
                sniff(
                    iface=interface,
                    prn=self._handle_packet,
                    store=False,
                    timeout=1
                )

        self._thread = threading.Thread(
            target=run,
            daemon=True
        )
        self._thread.start()

    def stop(self):

        if not self.is_running():
            return

        self._stop_event.set()

        if self._thread:
            self._thread.join(timeout=2)

        if self._hopper_thread:
            self._hopper_thread.join(timeout=2)

    def is_running(self):
        return self._thread is not None and self._thread.is_alive()

    def _extract_mac(self, packet):
        try:
            for field in ["addr2", "addr1", "addr3"]:
                if hasattr(packet, field):
                    mac = getattr(packet, field)
                    if mac:
                        return mac
        except Exception:
            pass
        return None

    def _handle_packet(self, packet):

        if self._stop_event.is_set():
            return

        mac = self._extract_mac(packet)

        packet_data = {
            "summary": packet.summary(),
            "mac": mac,
            "raw": packet
        }

        if self.on_packet:
            try:
                self.on_packet(packet_data)
            except Exception as e:
                print(f"Packet callback error: {e}")

# This is the End Of File - /services/packet_service.py