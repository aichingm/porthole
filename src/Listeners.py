# keyboard listener imports
from pynput import keyboard
# subprocess is needed to run dmenu
import subprocess
import _thread


class KbdListenerThread(object):
    def __init__(self, porthole):
        self._porthole = porthole
        self._keyCombination = {keyboard.Key.shift, keyboard.Key.ctrl, keyboard.Key.enter}
        self._current = set()

    def run(self):
        with keyboard.Listener(on_press=self.on_press, on_release=self.on_release) as listener:
            listener.join()

    def on_press(self, key):
        charKey = str(key)[1:-1].lower()
        if key in self._keyCombination or charKey in self._keyCombination:
            self._current.add(key)
            if ( all(k in self._current for k in self._keyCombination)
                 or charKey in self._keyCombination ) \
                    and self._porthole.web_engine_view.isActiveWindow():
                result = subprocess.run(['dmenu', '-p', "::"], stdin=subprocess.DEVNULL, stdout=subprocess.PIPE)
                if result.returncode == 0:
                    self._porthole.set_code(result.stdout.decode("utf-8").strip())

    def on_release(self, key):
        try:
            self._current.remove(key)
        except KeyError:
            pass

    def set_keys(self, set):
        keyboard.Listener.stop
        self._current.clear()
        self._keyCombination = set
        _thread.start_new_thread(self.run, ())


class StdinListenerThread(object):
    def __init__(self, porthole):
        self._porthole = porthole
        self._prompt = ":: "

    def run(self):
        while True:
            try:
                line = input().strip()
                if line is not "":
                    self._porthole.set_code(line)
            except EOFError:
                break

    def set_prompt(self, str):
        self._prompt = set