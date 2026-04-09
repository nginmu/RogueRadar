class AppController:
    def __init__(self, model):
        self.model = model

    def update_second_tab(self, text):
        self.model.set("second_tab_text", text)
