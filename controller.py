# This is /controller.py
# RR V3 iteration 001
#
# Written by ChatGPT & Claude
# Steered by Nginmu Mbetse
# May 7 2026

from services.ble_service import BLEService
from services.packet_service import PacketService
from services.replay_service import ReplayService
from services.interface_service import enable_monitor_mode, disable_monitor_mode
from services.packet_decoder import decode_type_subtype, extract_ssid
from scapy.layers.dot11 import Dot11
from scapy.layers.dot11 import RadioTap
import time
from core.event import Event

class AppController:

    def __init__(self, model, event_bus, event_logger=None, sqlite_sink=None):

        self.ble_service = BLEService()
        self.ble_service.on_device = self.handle_ble
        self.model = model
        self.event_bus = event_bus
        self.event_logger = event_logger
        self.sqlite_sink = sqlite_sink

        # DATA SOURCES
        self.packet_service = PacketService()
        self.replay_service = ReplayService(event_bus)
        self.packet_service.on_packet = self.handle_packet

        # STATE
        self.current_source = None
        self.current_interface = None
        self.current_protocol = None

    # LOGGER
    def toggle_logging(self):
        if self.event_logger:
            self.event_logger.toggle()

    def is_logging_enabled(self):
        return self.event_logger.enabled if self.event_logger else False

    # SQLITE
    def toggle_sqlite(self):
        if self.sqlite_sink:
            self.sqlite_sink.toggle()

    def is_sqlite_enabled(self):
        return self.sqlite_sink.enabled if self.sqlite_sink else False

    # SOURCE CONTROL
    def stop_current_source(self):

        if not self.current_source:
            return

        self.current_source.stop()

        if self.current_source == self.packet_service:
            disable_monitor_mode()
            self.current_interface = None

        self.current_source = None
        self.current_protocol = None

    def is_running(self):
        return self.current_source is not None

    # GENERIC SOURCE ENTRY
    def start_source(self, protocol, **kwargs):

        # Generic entry point for starting sources.

        if self.current_source:
            self.stop_current_source()

        if protocol == "wifi":
            interface = kwargs.get("interface")
            self.start_live_capture(interface)

        elif protocol == "ble":
            self.start_ble()

        elif protocol == "replay":
            filepath = kwargs.get("filepath", "events.log")
            speed = kwargs.get("speed", 1.0)
            self.start_replay(filepath, speed)

        else:
            print(f"Unknown protocol: {protocol}")

    # LIVE CAPTURE
    def start_live_capture(self, interface):

        try:
            mon_iface = enable_monitor_mode(interface)
        except Exception as e:
            print(f"Monitor mode error: {e}")
            return

        self.model.clear_devices("wifi")
        self.packet_service.start(mon_iface)
        self.current_source = self.packet_service
        self.current_interface = mon_iface
        self.current_protocol = "wifi"

    # REPLAY
    def start_replay(self, filepath="events.log", speed=1.0):

        if self.current_source:
            return

        self.model.clear_devices()
        self.replay_service.start(filepath, speed)
        self.current_source = self.replay_service
        self.current_protocol = "replay"

    # BLE start/stop
    def start_ble(self):

        self.model.clear_devices("ble")
        self.ble_service.start()
        self.current_source = self.ble_service
        self.current_protocol = "ble"

    # Handle BLE events
    def handle_ble(self, data):

        event = Event(
            type="ble.advert",
            source="ble_service",
            payload=data
        )

        self.event_bus.publish(event)

    # TOGGLES
    def toggle_live_capture(self, interface):

        if self.current_source == self.packet_service:
            self.stop_current_source()
        else:
            self.stop_current_source()
            self.start_live_capture(interface)

    def toggle_replay(self):

        if self.current_source == self.replay_service:
            self.stop_current_source()
        else:
            self.stop_current_source()
            self.start_replay()

    def is_live(self):
        return self.current_source == self.packet_service

    def is_replay(self):
        return self.current_source == self.replay_service

    # PACKET → EVENT
    def handle_packet(self, packet_data):

        mac = packet_data.get("mac")
        raw = packet_data.get("raw")

        if not mac:
            return

        pkt_type = "?"
        role = "Other"
        rssi = None

        # RSSI
        if raw and raw.haslayer(RadioTap):
            try:
                rssi = raw[RadioTap].dBm_AntSignal
            except Exception:
                pass

        # DOT11
        if raw and raw.haslayer(Dot11):
            try:
                dot11 = raw[Dot11]

                pkt_type = decode_type_subtype(dot11.type, dot11.subtype)

                if dot11.type == 0:
                    if dot11.subtype == 8:
                        role = "AP"
                    elif dot11.subtype == 4:
                        role = "Client"

                elif dot11.type == 2:
                    role = "Data"

            except Exception:
                pass

        ssid = extract_ssid(raw) if raw else ""

        event = Event(
            type="wifi.packet",
            source="packet_service",
            payload={
                "mac": mac,
                "packet_summary": packet_data.get("summary"),
                "ssid": ssid,
                "type": pkt_type,
                "role": role,
                "rssi": rssi,
            }
        )

        self.event_bus.publish(event)

# This is the End Of File - /controller.py
