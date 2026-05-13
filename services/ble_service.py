# This is /services/ble_service.py
# RR V3 iteration 001
#
# Written by ChatGPT & Claude
# Steered by Nginmu Mbetse
# May 7 2026

import threading
import asyncio
from bleak import BleakScanner

class BLEService:

    def __init__(self):
        self._thread = None
        self._loop = None
        self._stop_event = threading.Event()
        self.on_device = None

    # CONTROL
    def start(self):
        if self.is_running():
            return

        self._stop_event.clear()

        self._thread = threading.Thread(
            target=self._run_loop,
            daemon=True
        )
        self._thread.start()

    def stop(self):
        self._stop_event.set()

        if self._thread:
            self._thread.join(timeout=2)

    def is_running(self):
        return self._thread is not None and self._thread.is_alive()

    # THREAD
    def _run_loop(self):
        self._loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self._loop)

        try:
            self._loop.run_until_complete(self._scan())
        finally:
            self._loop.close()

    # SCAN
    async def _scan(self):

        def detection_callback(device, advertisement_data):

            if self._stop_event.is_set():
                return

            data = {
                "mac": device.address,
                "name": device.name or "",
                "rssi": advertisement_data.rssi,
            }

            if self.on_device:
                self.on_device(data)

        scanner = BleakScanner(detection_callback=detection_callback)
        await scanner.start()

        try:
            while not self._stop_event.is_set():
                await asyncio.sleep(0.5)
        finally:
            await scanner.stop()

# This is the End Of File - /services/ble_service.py