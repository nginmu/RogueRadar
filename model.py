class AppModel:
    def __init__(self):
        self.data = {"second_tab_text": "This is the Second Tab"}
        self.observers = []

    def set(self, key, value):
        self.data[key] = value
        self._notify_observers(key, value)

    def get(self, key):
        return self.data.get(key)

    def register_observer(self, observer):
        self.observers.append(observer)

    def _notify_observers(self, key, value):
        for observer in self.observers:
            observer.update(key, value)
