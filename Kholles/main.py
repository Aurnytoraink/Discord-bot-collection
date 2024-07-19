from pathlib import Path
import json
import discord
from discord import channel
import asyncio

##############

PATH = Path("YOUR PATH")

TOKEN = json.loads(open(PATH/"config.json",'rb').read())["token"]

#############
client = discord.Client()

classes_list = []
tipe_list = []

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')

@client.event
async def on_voice_state_update(member, before, after):

    if after.channel != None:
        if after.channel.id == YOUR_CHANNEL_ID:
            category = after.channel.category
            if member.nick is None:   name = member.name
            else:   name = member.nick


            voice = await member.guild.create_voice_channel(f"💬 {name}",user_limit=4,category=category)
            chat = await member.guild.create_text_channel(f"📝 {name}",category=category)
            await member.move_to(voice)

            classes_list.append([voice, chat])

            await asyncio.sleep(0.5)

        elif after.channel.id == YOUR_CHANNEL_ID:
            category = after.channel.category
            if member.nick is None:   name = member.name
            else:   name = member.nick

            
            voice = await member.guild.create_voice_channel(f"💬 TIPE {len(tipe_list)+1}",category=category)
            chat = await member.guild.create_text_channel(f"📝 TIPE {len(tipe_list)+1}",category=category)
            await member.move_to(voice)

            tipe_list.append([voice, chat])

            await asyncio.sleep(0.5)

    for i in range(len(classes_list)):
            if before.channel == classes_list[i][0]:
                if before.channel.members == []:
                    await classes_list[i][0].delete()
                    await classes_list[i][1].delete()
                    classes_list.pop(i)
    for i in range(len(tipe_list)):
        if before.channel == tipe_list[i][0]:
            if before.channel.members == []:
                await tipe_list[i][0].delete()
                await tipe_list[i][1].delete()
                tipe_list.pop(i)



client.run(TOKEN)
