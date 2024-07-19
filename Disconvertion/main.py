from pathlib import Path
import os
import shutil
import json
import requests

import discord

##############
PATH = Path("YOUR PATH")

if os.path.exists(PATH / 'files'):
    shutil.rmtree(PATH / "files")
os.makedirs(PATH / "files")

TOKEN = json.loads(open(PATH/"config.json",'rb').read())["token"]

ext_ref = ["doc","docx","odt","odf","odp","odg","ods","ott","xls","xlsx","ppt","pptx"]

##############
client = discord.Client()

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    
    if message.content == "ptdrtki?":
        await message.channel.send("🤖**Bip! Bop!** Je m'appelle Disconvertion. Mon rôle est d'automatiser les convertions de documents en fichier PDF")

    if message.attachments != []:
        attachment = message.attachments[0]
        extension = attachment.filename.split(".")[-1]
        output = ".".join(attachment.filename.split(".")[:len(attachment.filename.split("."))-1])+".pdf"
        if extension in ext_ref:
            data = requests.get(attachment.url).content
            with open(PATH/("files/"+attachment.filename),'xb') as f:
                f.write(data)

            os.system(f"libreoffice --headless --convert-to pdf \"{PATH/('files/'+attachment.filename)}\" --outdir \"{PATH/('files/')}\"")
            await message.channel.send("🤖**Bip! Bop!**\nVoici la version PDF :",file=discord.File(PATH/('files/'+output)))

            os.remove(PATH/("files/"+output))
            os.remove(PATH/("files/"+attachment.filename))


client.run(TOKEN)
