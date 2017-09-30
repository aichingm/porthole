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
        
    def border(self, border):
        if border:
            self._porthole.setWindowFlags(QtCore.Qt.WindowTitleHint)
        else:
            self._porthole.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self._porthole.show()
        return self
