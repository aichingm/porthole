# QT imports
from PyQt5 import QtCore
# url imports
from urllib.parse import urlparse
# system and os imports
import subprocess


class PortholeInstance():

    instance = None

    def __init__(self):
        pass

    def set_instance(instance):
        PortholeInstance.instance = instance


class PortholeProxy():

    def __init__(self, porthole):
        self._porthole = porthole

    def go(self, url):
        purl = urlparse(url)
        scheme = purl.scheme
        if scheme == '':
            url = "https://" + url
        self._porthole.web_engine_view.load(QtCore.QUrl(url))
        return self

    def back(self):
        self._porthole.web_engine_view.back()
        return self

    def forward(self):
        self._porthole.web_engine_view.forward()
        return self

    def reload(self):
        self._porthole.web_engine_view.reload()
        return self

    def nop(self):
        return self

    def dim(self, w, h):
        self._porthole.resize(w, h)
        self._porthole.show()
        return self

    def pos(self, left, top):
        self._porthole.move(left, top)
        self._porthole.show()
        return self

    def exit(self):
        self._porthole.exit()
        return self

    def wall(self, text):
        result = subprocess.run(['wall', str(text)], stdin=subprocess.DEVNULL,stdout=subprocess.PIPE)
        return self

    def border(self, border=None):
        if border == None:
             border = self._porthole.has_border()
        if not border:
            self._porthole.add_window_flag(QtCore.Qt.FramelessWindowHint)
        else:
            self._porthole.remove_window_flag(QtCore.Qt.FramelessWindowHint)
        self._porthole.show()
        return self

    def ontop(self, ontop=None):
        if ontop == None:
            ontop = not self._porthole.is_on_top()
        if ontop:
            if self._porthole.is_on_bottom():
                self._porthole.remove_window_flag(QtCore.Qt.WindowStaysOnBottomHint)
            self._porthole.add_window_flag(QtCore.Qt.WindowStaysOnTopHint)
        else:
            self._porthole.remove_window_flag(QtCore.Qt.WindowStaysOnTopHint)
        self._porthole.show()
        return self

    def onbottom(self, onbottom=None):
        if onbottom == None:
            onbottom = not self._porthole.is_on_bottom()
        if onbottom:
            if self._porthole.is_on_top():
                self._porthole.remove_window_flag(QtCore.Qt.WindowStaysOnTopHint)
            self._porthole.add_window_flag(QtCore.Qt.WindowStaysOnBottomHint)
        else:
            self._porthole.remove_window_flag(QtCore.Qt.WindowStaysOnBottomHint)
        self._porthole.show()
        return self

    def taskbar(self, taskbar=None):
        if taskbar == None:
            taskbar = self._porthole.is_taskbar()
        if not taskbar:
            self._porthole.add_window_flag(QtCore.Qt.Tool)
        else:
            self._porthole.remove_window_flag(QtCore.Qt.Tool)
        self._porthole.show()
        return self

    def fs(self, fullscreen=None):
        if fullscreen == None:
            fullscreen = not self._porthole.isFullScreen()

        print(fullscreen)
        if not fullscreen:
            self._porthole.showNormal()
        else:
            self._porthole.showFullScreen()
        return self

    def setaccess(self, key_seq=None):
        if key_seq == None:
            key_seq = "Ctrl+Shift+Return"
        self._porthole.set_key_sequence(key_seq)
        return self
