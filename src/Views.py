# QT imports
from PyQt5 import QtCore, QtGui
from PyQt5.QtWebEngineWidgets import QWebEngineView


class WebEngineView(QWebEngineView):
    def __init__(self):
        super(WebEngineView, self).__init__()
        self.setAcceptDrops(True)

    def dropEvent(self, event: QtGui.QDropEvent):
        self.load(QtCore.QUrl(event.mimeData().urls()[0]))

    def dragEnterEvent(self, event: QtGui.QDragEnterEvent):
        formats = event.mimeData().formats()
        if "text/uri-list" in formats and len(event.mimeData().urls()) == 1:
            event.accept()
        else:
            event.ignore()
