# This is /model.py
# RR V3 iteration 001
#
# Written by ChatGPT & Claude
# Steered by Nginmu Mbetse
# May 7 2026

class AppModel:

    def __init__(self, event_bus=None):

        # DEVICE STORES
        self.devices = {
            "wifi": {},
            "ble": {},
            "bt": {},
            "tpms": {},
            "ant": {},
        }

        # GENERIC DATA
        self.data = {
            "second_tab_text": "This is the Second Tab"
        }

        # IGNORE SYSTEM
        self.ignore_list = set()

        # OBSERVERS
        self.observers = []

        # EVENT BUS
        self.event_bus = event_bus

        if self.event_bus:
            self._subscribe_to_events()

    # EVENT SUBSCRIPTION
    def _subscribe_to_events(self):
        self.event_bus.subscribe_all(self._handle_event)

    def _handle_event(self, event):

        event_type = getattr(event, "type", "")
        payload = getattr(event, "payload", {})

        if not event_type or "." not in event_type:
            return

        protocol, subtype = event_type.split(".", 1)

        if protocol not in self.devices:
            return

        if not isinstance(payload, dict):
            return

        if self._should_ignore(payload):
            return

        # ROUTING
        if protocol == "wifi":
            self._handle_wifi_event(event)

        elif protocol == "ble":
            self._handle_ble_event(event)

    # WIFI
    def _handle_wifi_event(self, event):

        payload = event.payload
        now = event.timestamp

        mac = payload.get("mac")
        if not mac:
            return

        pkt_type = payload.get("type", "?")
        ssid = payload.get("ssid", "")
        role = payload.get("role", "Other")
        rssi = payload.get("rssi")
        store = self.devices["wifi"]
        is_new = mac not in store

        if is_new:
            device = {
                "mac": mac,
                "packet_count": 1,
                "first_seen": now,
                "last_seen": now,
                "type": pkt_type,
                "ssid": ssid,
                "role": role,
                "rssi": rssi,
            }

            store[mac] = device
            self._notify_observers(("wifi", mac), device, True)
            return

        device = store[mac]
        device["packet_count"] += 1
        device["last_seen"] = now

        if rssi is not None:
            device["rssi"] = rssi

        if pkt_type != "?":
            device["type"] = pkt_type

        if ssid:
            device["ssid"] = ssid

        if role != "Other":
            device["role"] = role

        self._notify_observers(("wifi", mac), device, False)

    # BLE
    def _handle_ble_event(self, event):

        payload = event.payload
        now = event.timestamp

        mac = payload.get("mac")
        if not mac:
            return

        store = self.devices["ble"]
        is_new = mac not in store

        if is_new:
            device = {
                "mac": mac,
                "name": payload.get("name", ""),
                "rssi": payload.get("rssi"),
                "first_seen": now,
                "last_seen": now,
            }

            store[mac] = device
            self._notify_observers(("ble", mac), device, True)
            return

        device = store[mac]
        device["rssi"] = payload.get("rssi")
        device["last_seen"] = now

        if payload.get("name"):
            device["name"] = payload.get("name")

        self._notify_observers(("ble", mac), device, False)

    # IGNORE SYSTEM
    def _should_ignore(self, payload):

        mac = payload.get("mac")

        if not mac:
            return False

        return mac in self.ignore_list

    def add_to_ignore(self, identifier):
        self.ignore_list.add(identifier)

    def remove_from_ignore(self, identifier):
        self.ignore_list.discard(identifier)

    def get_ignore_list(self):
        return self.ignore_list

    # DEVICE CONTROL
    def clear_devices(self, protocol=None):

        if protocol:
            if protocol in self.devices:
                self.devices[protocol].clear()
                self._notify_observers(("clear", protocol), None, True)
            return

        for proto in self.devices:
            self.devices[proto].clear()

        self._notify_observers(("clear", "all"), None, True)

    def get_devices(self, protocol=None):
        if protocol:
            return self.devices.get(protocol, {})
        return self.devices

    # GENERIC STORAGE
    def set(self, key, value):
        self.data[key] = value
        self._notify_observers(("data", key), value, False)

    def get(self, key):
        return self.data.get(key, None)

    # OBSERVER SYSTEM
    def register_observer(self, observer):
        if observer not in self.observers:
            self.observers.append(observer)

    def unregister_observer(self, observer):
        if observer in self.observers:
            self.observers.remove(observer)

    def _notify_observers(self, key, value, is_new):
        for observer in list(self.observers):
            try:
                observer.update(key, value, is_new)
            except Exception as e:
                print(f"Observer error: {e}")

# This is the End Of File - /model.py
