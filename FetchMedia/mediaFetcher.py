import tiktok
import insta
from reddit import Reddit
import os
import discord
from dotenv import load_dotenv
from urllib.parse import urlparse
from pathlib import Path

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
# The token key is load from the .env file
PATH = Path("/home/aurnytoraink/Projets/Code/Bot/FetchMedia/") # <= Set your path

if os._exists(PATH/"audio"):
    os.remove(PATH/"audio")
if os._exists(PATH/"video"):
    os.remove(PATH/"video")
if os._exists(PATH/"output.mp4"):
    os.remove(PATH/"output.mp4")

client = discord.Client()
redditClient = Reddit()

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    url = urlparse(message.content).netloc

    if url.startswith("vm.tiktok.com") or url.startswith("www.tiktok.com"):
        r = tiktok.downloadVideo(message.content)
    elif url.startswith("www.instagram.com"):
        r = insta.download(message.content)
    elif url.startswith("www.reddit.com"):
        r = redditClient.download(message.content)
    else:
        return

    if r:
        filename = message.content.split("/")[3]
        open(PATH/(filename+r[1]),'xb').write(r[0])
        if r[2]:
            file = discord.File(PATH/(filename+r[1]), spoiler=True)
        else:
            file = discord.File(PATH/(filename+r[1]))
        await message.channel.send(file=file)
        os.remove(PATH/(filename+r[1]))
    elif r is False:
        await message.channel.send("Désolé, le fichier est trop grand.\nVeuillez utiliser le lien.")
    elif r is None:
        await message.channel.send("Une erreur est survenue")

client.run(TOKEN)