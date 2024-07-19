import json
from pathlib import Path
import discord

##############

PATH = Path("")
# Insérer l'adresse où se situe votre dossier

TOKEN = json.loads(open(PATH/"config.json",'rb').read())["token"]

#############
client = discord.Client()

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')

@client.event
async def on_message(message):
    # Évite que le bot intercepte ces propres messages
    if message.author == client.user:
        return

    # Prise en charge des majuscules et mininuscules
    # + les textes déformés comme "qUoiiiiiiiiiiiiiiiii ?"
    if message.content.lower().startswith('quoi'):
        await message.channel.send("FEUR!!!!")

client.run(TOKEN)