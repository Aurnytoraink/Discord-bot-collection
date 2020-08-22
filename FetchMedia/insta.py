import requests
from urllib.parse import urlparse
from bs4 import BeautifulSoup
import json

def download(url):
    header = header = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36"}
    try:
        r = requests.get(url, headers=header)
    except:
        return None
    soup = BeautifulSoup(r.text, 'lxml')
    elements = soup.find_all('script')
    if len(elements) == 15:
        i = 4
    else:
        i = 3
    find = elements[i].next
    find = find.replace(';', '')
    find = find.replace('window._sharedData = ', '')
    find = find.replace('\\u0026', '&')
    find = json.loads(find)
    try:
        source = find["entry_data"]["PostPage"][0]["graphql"]["shortcode_media"]["video_url"]
        ext = ".mp4"
    except:
        source = find["entry_data"]["PostPage"][0]["graphql"]["shortcode_media"]["display_url"]
        ext = ".jpg"
    data = requests.get(source).content
    if len(data) < 8388190:
        return data, ext, False
    else:
        return False
