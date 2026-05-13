# This is /main.py
# RR V3 iteration 001
#
# Written by ChatGPT & Claude
# Steered by Nginmu Mbetse
# May 7 2026

from model import AppModel
from controller import AppController
from gui_window import AppWindow
from core.event_bus import EventBus
from core.event_logger import EventLogger
from services.sqlite_sink import SQLiteSink

def main():

    # CORE
    event_bus = EventBus()
    model = AppModel(event_bus=event_bus)

    # LOGGER
    logger = EventLogger(event_bus)

    # SQLITE SINK
    sqlite_sink = SQLiteSink()
    # Subscribe sink to event bus
    event_bus.subscribe_all(sqlite_sink.handle_event)

    # CONTROLLER
    controller = AppController(
        model,
        event_bus,
        logger,
        sqlite_sink
    )

    # UI
    app = AppWindow(controller, model)
    app.run()

if __name__ == "__main__":
    main()

# This is the End Of File - /main.py