import requests
import json


def getLyrics(title, album):
    url = "https://c.y.qq.com/lyric/fcgi-bin/fcg_query_lyric_new.fcg"
    headers = {"Referer": "https://y.qq.com/portal/player.html"}
    params = {
        "songmid": searchSong(title, album),
        "format": "json",
        "nobase64": "1"
    }
    result = requests.get(url, headers=headers, params=params)

    return json.loads(result.content)["lyric"]


def searchSong(title, album):
    url = "https://c.y.qq.com/soso/fcgi-bin/client_search_cp"
    params = {
        "w": title+" "+album,
        "format": "json"
    }
    result = json.loads(requests.get(url, params=params).content)
    songList = result["data"]["song"]["list"]

    return songList[0]["songmid"]
