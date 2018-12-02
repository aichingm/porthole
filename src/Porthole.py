# QT imports
from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QShortcut
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWebEngineWidgets import QWebEngineSettings
# system and os imports
import sys
import os
import subprocess
import threading
import _thread
import signal
import traceback
import tempfile
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
from Listeners import StdinListenerThread


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
        self._app = app
        self.proxy = PortholeProxy(self)

    def _setup(self):
        self._code_signal.connect(self._handle_code)

    def _setup_win(self):
        self.setWindowTitle('Porthole')
        scriptDir = os.path.dirname(os.path.realpath(__file__))
        self.setWindowIcon(QtGui.QIcon(scriptDir + os.path.sep + 'res/icon.png'))
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint|QtCore.Qt.Tool|QtCore.Qt.WindowStaysOnTopHint)
        self.setAttribute(QtCore.Qt.WA_NoSystemBackground, True)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground, True)
        self.resize(440, 240)

        self.shortcut = QShortcut(QtGui.QKeySequence("Ctrl+Shift+Return"), self)
        self.shortcut.activated.connect(self._on_seq_down)

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
        self.setWindowFlag(flag, False)
        #self.show()

    def add_window_flag(self, flag):
        self.setWindowFlag(flag, True)
        #self.show()

    def has_border(self):
        return (self.windowFlags() & QtCore.Qt.FramelessWindowHint) == QtCore.Qt.FramelessWindowHint

    def is_on_top(self):
        return (self.windowFlags() & QtCore.Qt.WindowStaysOnTopHint) == QtCore.Qt.WindowStaysOnTopHint

    def is_on_bottom(self):
        return (self.windowFlags() & QtCore.Qt.WindowStaysOnBottomHint) == QtCore.Qt.WindowStaysOnBottomHint

    def is_taskbar(self):
        return (self.windowFlags() & QtCore.Qt.Tool) == QtCore.Qt.Tool

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

    def set_listeners(self, listeners):
        self._listeners = listeners

    def find_listener(self, type):
        return next(l for l in self._listeners if isinstance(l, type))

    def _on_seq_down(self):
        t = threading.Thread(target=self._dmenu_tread)
        t.start()

    def _dmenu_tread(self):
        result = subprocess.run(['dmenu', '-p', "::"], stdin=subprocess.DEVNULL, stdout=subprocess.PIPE)
        if result.returncode == 0:
            self.set_code(result.stdout.decode("utf-8").strip())

    def set_key_sequence(self, str):
        self.shortcut.setKey(str)


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
    parser.add_argument("--init", action='append', help="code to initialize the porthole instance, can be passed multiple times")
    args = parser.parse_args()

    # register ctrl+c to SIGINT
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    app = QApplication(sys.argv)
    PortholeInstance.set_instance(Porthole(app))

    listeners = []

    stdinListener = StdinListenerThread(PortholeInstance.instance)
    _thread.start_new_thread(stdinListener.run, ())
    listeners.append(stdinListener)

    PortholeInstance.instance.set_listeners(listeners)

    if test_for_custom_proxy():
        spec = importlib.util.spec_from_file_location("", get_proxy_file_name())
        proxyModule = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(proxyModule)

    if args.init:
        for code in args.init:
            PortholeInstance.instance.set_code(code)
    sys.exit(app.exec_())
