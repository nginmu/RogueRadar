from model import AppModel
from controller import AppController
from gui_window import AppWindow

def main():
    model = AppModel()
    controller = AppController(model)
    app = AppWindow(controller, model)
    app.run()

if __name__ == "__main__":
    main()
