from pynput import keyboard
from testing_key_event import KeyEventLogger
from globals import NUMBER_SAMPLES


class KeyListener:

    def __init__(self):
        self.listener = keyboard.Listener(on_press=self.on_press, on_release=self.on_release)
        self.listener.start()
        self.listener.join()

    # def start(self):

    def stop(self):
        self.listener.stop()

    @staticmethod
    def on_press(key):
        instance = KeyEventLogger()
        try:
            # print('alphanumeric key {0} pressed'.format(
            #     key.char))
            instance.insert_pressed_event()
            # c = keyboard.Controller()
            # c.press(keyboard.Key.backspace)
        except AttributeError:
            print('special key {0} pressed'.format(key))

            # TODO: Should this be handled?

    @staticmethod
    def on_release(key):
        instance = KeyEventLogger()
        if instance.has_pressed():
            instance.insert_released_event()
            # print('{0} released'.format(key))
            if key == keyboard.Key.enter:
                cond = instance.calculate()
                # Stops the listener
                if cond:
                    return False
                else:
                    print("The last attempt was ignored. Type your password again\n")
