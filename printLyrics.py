from metadata import md
import lyrics.qqmusic
import time
from datetime import datetime
from PyQt5.QtWidgets import QLabel
from PyQt5.QtCore import *
from threading import Thread


class Lyrics():
    def loopPrint(self, thread):
        clock = Thread(target=self.clockRun) #异步计时，防止阻塞导致延迟
        clock.start()
        while True:
            self.status = md.PlaybackStatus()
            if self.status == "Paused":
                continue
            elif self.status == "Playing":
                self.curMetadata = md.Current()
                if self.curMetadata["title"] != self.lastMetadata["title"]:
                    self.lastMetadata = self.curMetadata
                    self.getLyrics()
                    self.time = 0
                for lyric in self.lyricsDict.get(self.time, []):
                    thread.signal.emit(lyric)
            time.sleep(0.05)

    # 计时线程
    def clockRun(self):
        while True:
            time.sleep(0.1)
            if self.status == "Playing":
                self.time = self.time+1
    
    def getLyrics(self):
        if self.curMetadata:
            lyricsObj = lyrics.qqmusic.getLyrics(self.curMetadata["title"],
                                            self.curMetadata["album"])

            lyricsList = lyricsObj.splitlines()
            self.lyricsDict = {}
            for line in lyricsList:
                lineSplited = line.split("]")
                timeLine = lineSplited[0][1:]
                lyricsLine = lineSplited[1]
                if lyricsLine:
                    timeObj = datetime.strptime(timeLine, "%M:%S.%f")
                    microsec = timeObj.minute*60000+timeObj.second*1000+timeObj.microsecond/1000
                    key = int(microsec/100)
                    if key not in self.lyricsDict:
                        self.lyricsDict[key] = [lyricsLine]
                    else:
                        self.lyricsDict[key].append(lyricsLine)


    def show(self, thread):
        self.status = "Paused"
        self.time = 0
        self.lastMetadata = md.Current()
        self.curMetadata = self.lastMetadata
        self.getLyrics()
        self.loopPrint(thread)