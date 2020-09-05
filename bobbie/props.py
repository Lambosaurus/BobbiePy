import time

class LiveProperty():
    def __init__(self):
        self.value = None
        self.__subscribers = {}
    
    def subscribe(self, callback, on_change = False):
        self.__subscribers[callback] = not on_change

    def unsubscribe(self, callback):
        self.__subscribers.pop(callback)
    
    def _update(self, value):
        changed = self.value != value
        self.value = value
        for subs, always_notify in list(self.__subscribers.items()):
            if always_notify or changed:
                subs(value)
