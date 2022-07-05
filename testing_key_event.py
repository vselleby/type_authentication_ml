import time
from database_handler import DatabaseHandler


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class KeyEventLogger(metaclass=Singleton):
    def __init__(self):
        self.current_milli_time = lambda: int(round(time.time() * 1000))
        self.pressed_array = []
        self.released_array = []
        self.db_handler = DatabaseHandler()
        self.last_event = 0
        self.authenticate = False

    def calculate(self):
        # Remove last enter click from equation
        self.pressed_array.pop(-1)
        self.released_array.pop(-1)
        for pressed_time in self.pressed_array:
            print(pressed_time)
        for released_time in self.released_array:
            print(released_time)

        if self.authenticate:
            cond = self.db_handler.authenticate(self.pressed_array, self.released_array)
        else:
            cond = self.db_handler.register(self.pressed_array, self.released_array)

        self.pressed_array = []
        self.released_array = []
        return cond

    def insert_pressed_event(self):
        if len(self.pressed_array) == 0:
            self.last_event = 0
            self.pressed_array.insert(0, 0)
        else:
            self.pressed_array.insert(len(self.pressed_array), self.current_milli_time() - self.last_event)
        self.last_event = self.current_milli_time()

    def insert_released_event(self):
        if len(self.pressed_array) != 0:
            self.released_array.insert(len(self.released_array), self.current_milli_time() - self.last_event)
            self.last_event = self.current_milli_time()

            # def backspace_clicked(self):
            # self.pressed_array.pop(-1)
            # self.released_array.pop(-1)

    def mode(self, bool_auth):
        if bool_auth:
            self.authenticate = True
        else:
            self.authenticate = False

    def has_pressed(self):
        return len(self.pressed_array)
