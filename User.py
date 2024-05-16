class User:
    def __init__(self, name, pin):
        self.name = name
        self.pin = pin

    def authenticate(self, entered_pin):
        return self.pin == entered_pin
