from testing_key_event import KeyEventLogger
from key_listener import KeyListener
from database_handler import DatabaseHandler
from globals import NUMBER_SAMPLES


class UserHandler:

    def __init__(self):
        self.logger = KeyEventLogger()

    def new_user(self):
        self.logger.mode(0)
        db = DatabaseHandler()
        cond = False
        while not cond:
            username = input("Type desired username\n")
            cond = db.check_available(username)
            if not cond:
                print("Username not available, try another one\n")
            else:
                print("Username available!")
        print("Type your password " + str(NUMBER_SAMPLES) + " times\n")
        i = 0
        while i < NUMBER_SAMPLES:
            listener = KeyListener()
            i += 1
            if i != NUMBER_SAMPLES:
                input("Type your password again, only " + str(NUMBER_SAMPLES - i) + " times left\n")
            listener.stop()

    def authenticate_user(self):
        self.logger.mode(1)
        db = DatabaseHandler()
        cond = True
        while cond:
            username = input("Type your username\n")
            cond = db.check_available(username)
            if cond:
                print("Username does not exist")
        print("Type your password")
        listener = KeyListener()
        listener.stop()
