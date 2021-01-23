import platform
import win32gui
import win32api
import os


class BaseMetadata():
    def Current(self):
        return None
    
    def PlaybackStatus(self):
        return None

class LinuxMetadata(BaseMetadata):
    def __init__(self):
        import dbus
        try:
            session_bus = dbus.SessionBus()
            spotify_bus = session_bus.get_object("org.mpris.MediaPlayer2.spotify",
                                                    "/org/mpris/MediaPlayer2")
            self.spotify_properties = dbus.Interface(spotify_bus,
                                                "org.freedesktop.DBus.Properties")
        except:
            print("Cannot find spotify running.")

    def Current(self):
        try:
            data = self.spotify_properties.Get("org.mpris.MediaPlayer2.Player", "Metadata")
            return {"title": data["xesam:title"], "album": data["xesam:album"]}
        except:
            return None

    def PlaybackStatus(self):
        try:
            return self.spotify_properties.Get("org.mpris.MediaPlayer2.Player", "PlaybackStatus")
        except:
            return "Not running"


class WindowsMetadata(BaseMetadata):
    def __init__(self):
        self.winId = win32gui.FindWindow("SpotifyMainWindow", None)

    def Current(self):
        info = win32gui.GetWindowText(self.winId)
        print(info)
        self.artist, self.title = info.split(" - ",1)
        return {"title": self.title.strip(), "album": self.artist.strip()}
    
    def PlaybackStatus(self):
        return self.title is None


def getMetadata():
    operationSystem = platform.system()
    if operationSystem == "Linux":
        return LinuxMetadata()
    elif operationSystem == "Windows":
        return WindowsMetadata()
    else:
        return BaseMetadata()
        
md = getMetadata()