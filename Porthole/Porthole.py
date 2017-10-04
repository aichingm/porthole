#QT imports
from PyQt5 import QtCore, QtGui, QtWebEngine, QtWebEngineWidgets, QtWebEngineCore
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QGuiApplication
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEngineSettings
#keyboard listener imports
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
#path imports
import os.path
from pathlib import Path
#modul loading imports
import importlib.util
#porthole imports
from PortholeProxy import PortholeProxy, PortholeInstance



class Porthole(QMainWindow):
   
    _code_signal = pyqtSignal()
    
    def __init__(self, app):
        super().__init__()
        self._setupVars(app)
        self._setupWin()
        self._setup()
        self._setupWebEngineVewiew();
        self.show();


    def _setupVars(self, app):
        self._code = ""
        self.isFs = False
        #                          remove the frame         put it over all other windows   remove it from the taskbar
        self.windowFlags = (QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowStaysOnTopHint | QtCore.Qt.Tool)
        self._app = app
        self.proxy = PortholeProxy(self)
        
    def _setup(self):
        self._code_signal.connect(self._handle_code)
        
    def _setupWin(self):
        self.setWindowTitle('Porthole')
        scriptDir = os.path.dirname(os.path.realpath(__file__))
        self.setWindowIcon(QtGui.QIcon(scriptDir + os.path.sep + 'res/icon.png'))
        # QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowStaysOnTopHint | QtCore.Qt.Tool
        self.setWindowFlags(self.windowFlags)
        self.setAttribute(QtCore.Qt.WA_NoSystemBackground, True)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground, True)
        self.resize(440, 240)

    def _setupWebEngineVewiew(self):
        self.webEngineVew = QWebEngineView()
        self.setCentralWidget(self.webEngineVew)
        print('file://'+self.getStartPage())
        self.webEngineVew.load(QtCore.QUrl('file://'+self.getStartPage()))
        self.webEngineVew.settings().setAttribute(QWebEngineSettings.FullScreenSupportEnabled, True)
        self.webEngineVew.page().fullScreenRequested.connect(lambda request: self._handle_fullscreenRequst(request))
        self.webEngineVew.loadFinished.connect(lambda data: self._handle_pageLoaded(data))
        self.webEngineVew.setAttribute(QtCore.Qt.WA_NoSystemBackground, True)
        self.webEngineVew.setAttribute(QtCore.Qt.WA_TranslucentBackground, True)
        #https://bugreports.qt.io/browse/QTBUG-41960
        self.webEngineVew.page().setBackgroundColor(QtCore.Qt.transparent)
       
    @QtCore.pyqtSlot()
    def _handle_code(self):
        try:
            eval("ph." + self._code , globals(), {"ph" : self.proxy})
        except Exception:
            traceback.print_exc()

    def getStartPage(self):
        scriptDir = os.path.dirname(os.path.realpath(__file__))
        return scriptDir + os.path.sep + 'res/Porthole.html'
        
    def setProxy(self, proxy):
            self.proxy = proxy
            
    def setCode(self, code):
        self._code = code
        self._code_signal.emit()
        
    def exit(self):
        self._app.quit()

    def removeWindowFlag(self, flag):
        self.windowFlags = self.windowFlags & ~flag
        self.setWindowFlags(self.windowFlags)
        self.show()
    
    def setWindowFlag(self, flag):
        self.windowFlags = self.windowFlags | flag
        self.setWindowFlags(self.windowFlags)
        self.show()
        
    def hasBorder(self):
        return (self.windowFlags & QtCore.Qt.FramelessWindowHint) == QtCore.Qt.FramelessWindowHint
    
    def isOnTop(self):
        return (self.windowFlags & QtCore.Qt.WindowStaysOnTopHint) == QtCore.Qt.WindowStaysOnTopHint
    
    def isTaskbar(self):
        return (self.windowFlags & QtCore.Qt.Tool) == QtCore.Qt.Tool
    
    def isFullScreen(self):
        return self.isFs

    def showFullScreen(self):
        self.isFs = True
        return super().showFullScreen()
    
    def showNormal(self):
        self.isFs = False
        return super().showNormal()

    def _handle_fullscreenRequst(self, request):
        request.accept()
        
    def _handle_pageLoaded(self, request):
        self.setWindowTitle(self.webEngineVew.page().title())
        

class ListenerThread():
    
    def __init__(self, porthole):
        self._porthole = porthole
        self._keyCombination = { keyboard.Key.shift, keyboard.Key.ctrl, keyboard.Key.enter }
        self._current = set()

    def run(self):
        with keyboard.Listener(on_press=self.on_press, on_release=self.on_release) as listener:
            listener.join()
    
    def on_press(self, key):
        if key in self._keyCombination:
            self._current.add(key)
            if all(k in self._current for k in self._keyCombination) and self._porthole.webEngineVew.isActiveWindow():
                result = subprocess.run(['dmenu', '-p', "::"], stdin=subprocess.DEVNULL,stdout=subprocess.PIPE)
                print(result)
                if result.returncode == 0:
                    self._porthole.setCode(result.stdout.decode("utf-8"))
                
    def on_release(self, key):
        try:
            self._current.remove(key)
        except KeyError:
            pass

def testForDmenu():
    result = subprocess.run(['which', 'dmenu'], stdout=subprocess.PIPE)
    return result.returncode == 0

def testCustomProxy():
    return os.path.isfile(getProxyFileName())
        
def getProxyFileName():
    home = str(Path.home())
    return home+"/.phuserproxy.py"

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--init", help="code to initialize the porthole instance")
    args = parser.parse_args()

    #reqister ctrl+c to siGINT
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    app = QApplication(sys.argv)
    PortholeInstance.setInstance(Porthole(app))
    if testForDmenu():
        kblistener = ListenerThread(PortholeInstance.instance)
        _thread.start_new_thread(kblistener.run, ())
    if testCustomProxy():
        spec = importlib.util.spec_from_file_location("", getProxyFileName())
        proxyModule = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(proxyModule)
    if args.init:
        PortholeInstance.instance.setCode(args.init)
    sys.exit(app.exec_())
