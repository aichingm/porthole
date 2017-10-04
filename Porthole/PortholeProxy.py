#QT imports
from PyQt5 import QtCore
#url imports
from urllib.parse import urlparse
#system and os imports
import subprocess  
   
class PortholeInstance():
    
    instance = None
    
    def __init__(self):
        pass
    
    def setInstance(instance):
        PortholeInstance.instance = instance

class PortholeProxy():
    
    def __init__(self, porthole):
        self._porthole = porthole
        
    def go(self, url):
        if not hasattr(urlparse(url), 'schema'):
            url = "https://" + url
        self._porthole.webEngineVew.load(QtCore.QUrl(url))
        return self
    
    def back(self):
        self._porthole.webEngineVew.back()
        return self
    
    def forward(self):
        self._porthole.webEngineVew.forward()
        return self
    
    def reload(self):
        self._porthole.webEngineVew.reload()
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
             border = self._porthole.hasBorder()
        if not border:
            self._porthole.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        else:
            self._porthole.removeWindowFlag(QtCore.Qt.FramelessWindowHint)
        return self

    def ontop(self, ontop=None):
        if ontop == None:
            ontop = not self._porthole.isOnTop()
        if ontop:
            self._porthole.setWindowFlag(QtCore.Qt.WindowStaysOnTopHint)
        else:
            self._porthole.removeWindowFlag(QtCore.Qt.WindowStaysOnTopHint)
        return self

    def taskbar(self, taskbar=None):
        if taskbar == None:
            taskbar = self._porthole.isTaskbar()
        if not taskbar:
            self._porthole.setWindowFlag(QtCore.Qt.Tool)
        else:
            self._porthole.removeWindowFlag(QtCore.Qt.Tool)
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
