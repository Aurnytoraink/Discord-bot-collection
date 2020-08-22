import os
import discord
import requests
from dotenv import load_dotenv

# The token key is load from the .env file
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

client = discord.Client()

listExtension = ["png","jpg","svg", "PNG", "JPG", "SVG"]

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    
    def compression(file):
        os.system("convert -quality 1% "+file+" output.jpg")
        return

    files = message.attachments
    if files:
        if message.content.startwith("!kompress"):
            url = (message.attachments[0].url)
            imgName = url.split("/")[6]
            extension = imgName.split(".")[1]
            if extension in listExtension:
                img = requests.get(url).content
                open(imgName, 'xb').write(img)
                compression(imgName)
                img = discord.File("output.jpg")
                await message.channel.send(file=img)
                os.system("rm "+imgName+" output.jpg")

        

client.run(TOKEN)