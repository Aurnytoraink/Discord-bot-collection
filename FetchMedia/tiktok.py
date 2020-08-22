import requests
from urllib.parse import urlparse
from bs4 import BeautifulSoup
import json

def downloadVideo(url):
    header = header = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36"}
    try:
        r = requests.get(url, headers=header)
    except:
        return None
    soup = BeautifulSoup(r.text, 'lxml')
    videofind = json.loads(soup.find(id="__NEXT_DATA__").string)
    videoSrc = videofind["props"]["pageProps"]["videoData"]["itemInfos"]["video"]["urls"][0]
    videoData = requests.get(videoSrc).content
    if len(videoData) < 8388190: #This condition verify that the video don't overpass the discord standar file limit
        return videoData, '.mp4', False
    else:
        return False