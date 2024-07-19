import praw
import requests
from pathlib import Path
import os

PATH = Path("") # <= Set your path
PATH.absolute().as_posix

class Reddit:
    def __init__(self):
        self.reddit = praw.Reddit(client_id="set your info",
                                  client_secret="set your info",
                                  user_agent="linux:FetchMedia:v1 (by u/your reddit username)")
    
    def download(self, url):
        submission = self.reddit.submission(url=url)
        if submission.over_18:
            nsfw = True
        else:
            nsfw =  False


        if submission.is_video:
            location = submission.media['reddit_video']['fallback_url']
            audiolocation = "/".join(submission.media['reddit_video']['fallback_url'].split("/")[:4]) + "/audio"
            data = requests.get(location).content
            dataAudio = requests.get(audiolocation)
            if dataAudio.ok:
                if (len(data) + len(dataAudio.content)) < 8388190: #Max upload file size
                    open(PATH/"video",'xb').write(data)
                    open(PATH/"audio",'xb').write(dataAudio.content)
                    os.system("ffmpeg -hide_banner -loglevel warning -i "+(PATH/"video").as_posix()+" -i "+(PATH/"audio").as_posix()+" -c:v copy -c:a aac -preset veryslow "+(PATH/"output.mp4").as_posix())
                    data = open(PATH/"output.mp4",'rb').read()
                    os.remove(PATH/"video")
                    os.remove(PATH/"audio")
                    os.remove(PATH/"output.mp4")
                    return data, '.mp4', nsfw
                else:
                    return False
            if len(data) < 8388190:
                return data, '.mp4', nsfw
            else:
                return False
        elif submission.is_reddit_media_domain:
            location = submission.preview['images'][0]['source']['url']
            data = requests.get(location).content
            return data, '.png', nsfw
        else:
            return


