import sys  
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import Ui_lyrics
from printLyrics import Lyrics


class LyricsWidget(QWidget):
    _startPos = None
    _endPos = None
    _isTracking = False
 
    def __init__(self):
        super().__init__()
        ui = Ui_lyrics.Ui_Form()
        ui.setupUi(self)
        self.label = ui.label
        self.thread = Thread_Lyrics()
        self.thread.signal.connect(self.callback)
        self.thread.start()

    def callback(self,lyric):
        self.label.setText(lyric)
 
    def mouseMoveEvent(self, e: QMouseEvent):
        self._endPos = e.pos() - self._startPos
        self.move(self.pos() + self._endPos)
 
    def mousePressEvent(self, e: QMouseEvent):
        if e.button() == Qt.LeftButton:
            self._isTracking = True
            self._startPos = QPoint(e.x(), e.y())
 
    def mouseReleaseEvent(self, e: QMouseEvent):
        if e.button() == Qt.LeftButton:
            self._isTracking = False
            self._startPos = None
            self._endPos = None


class Thread_Lyrics(QThread):
    signal = pyqtSignal(str)
    def __init__(self):
        super().__init__()

    def run(self):
        lyrics = Lyrics()
        lyrics.show(self)