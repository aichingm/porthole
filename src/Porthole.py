# QT imports
from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWebEngineWidgets import QWebEngineSettings
# keyboard listener imports
from pynput import keyboard
# system and os imports
import sys
import os
import subprocess
import _thread
import signal
import traceback
import time
import argparse
# path imports
import os.path
from pathlib import Path
# module loading imports
import importlib.util
# porthole imports
from PortholeProxy import PortholeProxy, PortholeInstance
from Views import WebEngineView


class Porthole(QMainWindow):
    _code_signal = pyqtSignal()

    def __init__(self, app):
        super().__init__()
        self._setup_vars(app)
        self._setup_win()
        self._setup()
        self._setup_web_engine_view()
        self.show()

    def _setup_vars(self, app):
        self._code = ""
        self.isFs = False
        #                          remove the frame         put it over all other windows   remove it from the taskbar
        self.windowFlags = (QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowStaysOnTopHint | QtCore.Qt.Tool)
        self._app = app
        self.proxy = PortholeProxy(self)

    def _setup(self):
        self._code_signal.connect(self._handle_code)

    def _setup_win(self):
        self.setWindowTitle('Porthole')
        scriptDir = os.path.dirname(os.path.realpath(__file__))
        self.setWindowIcon(QtGui.QIcon(scriptDir + os.path.sep + 'res/icon.png'))
        # QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowStaysOnTopHint | QtCore.Qt.Tool
        self.setWindowFlags(self.windowFlags)
        self.setAttribute(QtCore.Qt.WA_NoSystemBackground, True)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground, True)
        self.resize(440, 240)

    def _setup_web_engine_view(self):
        self.web_engine_view = WebEngineView()
        self.setCentralWidget(self.web_engine_view)
        self.web_engine_view.load(QtCore.QUrl('file://' + self.get_start_page()))
        self.web_engine_view.settings().setAttribute(QWebEngineSettings.FullScreenSupportEnabled, True)
        self.web_engine_view.page().fullScreenRequested.connect(lambda request: self._handle_fullscreen_requst(request))
        self.web_engine_view.loadFinished.connect(lambda data: self._handle_page_loaded(data))
        self.web_engine_view.setAttribute(QtCore.Qt.WA_NoSystemBackground, True)
        self.web_engine_view.setAttribute(QtCore.Qt.WA_TranslucentBackground, True)
        # https://bugreports.qt.io/browse/QTBUG-41960
        self.web_engine_view.page().setBackgroundColor(QtCore.Qt.transparent)

    @QtCore.pyqtSlot()
    def _handle_code(self):
        try:
            eval("ph." + self._code, globals(), {"ph": self.proxy})
        except Exception:
            traceback.print_exc()

    def get_start_page(self):
        scriptDir = os.path.dirname(os.path.realpath(__file__))
        return scriptDir + os.path.sep + 'res/Porthole.html'

    def set_proxy(self, proxy):
        self.proxy = proxy

    def set_code(self, code):
        self._code = code
        self._code_signal.emit()

    def exit(self):
        self._app.quit()

    def remove_window_flag(self, flag):
        self.windowFlags = self.windowFlags & ~flag
        self.setWindowFlags(self.windowFlags)
        self.show()

    def setWindowFlag(self, flag):
        self.windowFlags = self.windowFlags | flag
        self.setWindowFlags(self.windowFlags)
        self.show()

    def has_border(self):
        return (self.windowFlags & QtCore.Qt.FramelessWindowHint) == QtCore.Qt.FramelessWindowHint

    def is_on_top(self):
        return (self.windowFlags & QtCore.Qt.WindowStaysOnTopHint) == QtCore.Qt.WindowStaysOnTopHint

    def is_taskbar(self):
        return (self.windowFlags & QtCore.Qt.Tool) == QtCore.Qt.Tool

    def isFullScreen(self):
        return self.isFs

    def showFullScreen(self):
        self.isFs = True
        return super().showFullScreen()

    def showNormal(self):
        self.isFs = False
        return super().showNormal()

    def _handle_fullscreen_requst(self, request):
        request.accept()

    def _handle_page_loaded(self, request):
        self.setWindowTitle(self.web_engine_view.page().title())

    def closeEvent(self, event):
        QtCore.QCoreApplication.instance().quit()


class KbdListenerThread():
    def __init__(self, porthole):
        self._porthole = porthole
        self._keyCombination = {keyboard.Key.shift, keyboard.Key.ctrl, keyboard.Key.enter}
        self._current = set()

    def run(self):
        with keyboard.Listener(on_press=self.on_press, on_release=self.on_release) as listener:
            listener.join()

    def on_press(self, key):
        if key in self._keyCombination:
            self._current.add(key)
            if all(k in self._current for k in
                   self._keyCombination) and self._porthole.web_engine_view.isActiveWindow():
                result = subprocess.run(['dmenu', '-p', "::"], stdin=subprocess.DEVNULL, stdout=subprocess.PIPE)
                print(result)
                if result.returncode == 0:
                    self._porthole.set_code(result.stdout.decode("utf-8").strip())

    def on_release(self, key):
        try:
            self._current.remove(key)
        except KeyError:
            pass


class StdinListenerThread():
    def __init__(self, porthole):
        self._porthole = porthole

    def run(self):
        while True:
            line = input()
            self._porthole.set_code(line.strip())


def test_for_dmenu():
    result = subprocess.run(['which', 'dmenu'], stdout=subprocess.PIPE)
    return result.returncode == 0


def test_for_custom_proxy():
    return os.path.isfile(get_proxy_file_name())


def get_proxy_file_name():
    home = str(Path.home())
    return home + "/.phuserproxy.py"


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--init", help="code to initialize the porthole instance")
    args = parser.parse_args()

    # register ctrl+c to SIGINT
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    app = QApplication(sys.argv)
    PortholeInstance.set_instance(Porthole(app))

    if test_for_dmenu():
        kbdlistener = KbdListenerThread(PortholeInstance.instance)
        _thread.start_new_thread(kbdlistener.run, ())

    stdinListener = StdinListenerThread(PortholeInstance.instance)
    _thread.start_new_thread(stdinListener.run, ())

    if test_for_custom_proxy():
        spec = importlib.util.spec_from_file_location("", get_proxy_file_name())
        proxyModule = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(proxyModule)

    if args.init:
        PortholeInstance.instance.set_code(args.init)
    sys.exit(app.exec_())