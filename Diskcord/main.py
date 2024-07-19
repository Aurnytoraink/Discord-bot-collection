import gdrive
import os
import shutil
import discord
from pathlib import Path
from discord.ext import commands
from dotenv import load_dotenv
import asyncio

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
# The token key is load from the .env file

FFMPEG_PATH = "/usr/bin/ffmpeg"
PATH = Path("") # <= Set yout path

# discord.opus.load_opus()
voicechannel = []
bot = commands.Bot(command_prefix='$')

# Loads modules
service = gdrive.login()

# Reset cache music
if os.path.exists(PATH / 'musics'):
    shutil.rmtree(PATH / "musics")
os.makedirs(PATH / "musics")

@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')


@bot.command(name="join", help="Invite le bot dans un salon vocal")
async def join(ctx):
    user = ctx.message.author
    if user.voice is not None:
        place = len(voicechannel)
        voicechannel.append([await user.voice.channel.connect(timeout=100),[],0])
        voicechannel[place][0].play((discord.FFmpegPCMAudio(PATH / "connected_sound.opus", executable=FFMPEG_PATH)))

#TODO Corriger pour que le titre de la musique s'afficher à chaque fois qu'il passe à la suivante
#TODO Ne laisser passer que les liens Google, Nextcloud
@bot.command(name="play", help="Lien de la (ou les) musique(s) à jouer")
async def play(ctx, *args):
    user = ctx.message.author
    def check_playlist(vc):
        if vc[1] != [] and vc[2] < len(vc[1]) - 1:
            vc[2] += 1
            currentMusic = vc[1][vc[2]][0]
            gdrive.downloadMedia(service, currentMusic, str(id))
            # task = asyncio.ensure_future(ctx.send("**Je chante🎶: **" + currentMusicName + "\n**Queue:** {}/{}".format((vc[2]+1),len(vc[1]))))
            # print(task)
            vc[0].play(discord.FFmpegPCMAudio(PATH / ("musics/"+str(id)+'/'+currentMusic), executable=FFMPEG_PATH), after=lambda e: check_playlist(vc))
            return

    try:
        voicechannel.append([await user.voice.channel.connect(timeout=100),[],0])
    except AttributeError:
        await ctx.send("**Hmmm... Vous n'êtes pas connecté à un salon vocal !**")
    except discord.errors.ClientException:
        pass
    for vc in voicechannel:
        if vc[0].channel == user.voice.channel:
            if len(args) == 0:
                if vc[0].is_paused() or vc[0].is_playing():
                    if vc[0].is_paused():
                        vc[0].resume()
                        return
                    else:
                        await ctx.send("Âllo ? Vous m'entendez ?\nLa musique est déjà en cours de lecture !")
                        return
                else:
                    await ctx.send("-え？\nJe dois jouer quelle musique ?")
                    return
            elif args[0] == "random":
                queuedlist = gdrive.getMedias(service, args[1], True)
            elif args[0] == "add":
                if args[1] == "random":
                    queuedlist = gdrive.getMedias(service, args[2], True)
                else:
                    queuedlist = gdrive.getMedias(service, args[1])
                if queuedlist is None:
                    await ctx.send("**Aucune musique trouvée !**")
                    return
                vc[1] += queuedlist
                await ctx.send("**Youpi!** J'ai ajouté votre dossier à la queue.")
                return
            else:
                queuedlist = gdrive.getMedias(service, args[0])
            if queuedlist is None:
                await ctx.send("Aucune musique trouvée !")
                return
            if vc[0].is_playing:
                vc[1] = []
                vc[2] = 0
                vc[0].stop()
            await asyncio.sleep(1)
            await ctx.send("**Chargement...**")
            vc[1] = queuedlist
            id = vc[0].channel.id
            currentMusic = vc[1][vc[2]][0]
            currentMusicName = vc[1][vc[2]][1]
            gdrive.downloadMedia(service, currentMusic, str(id))
            await ctx.send("**Je chante🎶: **" + currentMusicName + "\n**Queue:** {}/{}".format((vc[2]+1),len(vc[1])))
            vc[0].play(discord.FFmpegPCMAudio(PATH / ("musics/"+str(id)+'/'+currentMusic), executable=FFMPEG_PATH), after=lambda e: check_playlist(vc))
        else:
            place = len(voicechannel)
            voicechannel.append([await user.voice.channel.connect(timeout=100),[],0])
            voicechannel[place][0].play((discord.FFmpegPCMAudio(PATH / "connected_sound.opus", executable=FFMPEG_PATH)))

@bot.command(name="np", aliases=["display","current"], help="Affiche la musique en cours")
async def np(ctx):
    user=ctx.message.author
    for vc in voicechannel:
        if vc[0].channel == user.voice.channel:
            if vc[0].is_playing():
                await ctx.send("**Je chante🎶: **" + vc[1][vc[2]][1] + "\n**Queue:** {}/{}".format((vc[2]+1),len(vc[1])))
            else:
                await ctx.send("**Aïe Aïe Aïe !** Je joue pas de musique actuellement")

@bot.command(name="add", help="Rajoute la (ou les) musique(s) à la queue actuelle")
async def add(ctx, *args):
    user=ctx.message.author
    for vc in voicechannel:
        if vc[0].channel == user.voice.channel:
            if len(args) == 0:
                await ctx.send("-え？\nJe dois rajouter quelle musique ?")
                return
            elif args[0] == "random":
                queuedlist = gdrive.getMedias(service, args[1], True)
            else:
                queuedlist = gdrive.getMedias(service, args[0])
            if queuedlist is None:
                await ctx.send("**Aucune musique trouvée !**")
                return
            vc[1] += queuedlist
            await ctx.send("**Youpi!** J'ai ajouté votre dossier à la queue.")

@bot.command(name="pause", help='Met en pause la musique')
async def pause(ctx):
    user=ctx.message.author
    for vc in voicechannel:
        if vc[0].channel == user.voice.channel:
            if vc[0].is_paused():
                vc[0].resume()
            else:
                vc[0].pause()
        else:
            await ctx.send("Vous n'êtes pas dans un salon vocal !")

@bot.command(name="resume", help='Fonction inverse de $pause') #TODO Prevent user if there is not music playing
async def resume(ctx):
    user=ctx.message.author
    for vc in voicechannel:
        if vc[0].channel == user.voice.channel:
            if vc[0].is_paused():
                vc[0].resume()
            else:
                await ctx.send("Âllo ? Vous m'entendez ?\nLa musique est déjà en cours de lecture !")
        else:
            await ctx.send("Vous n'êtes pas dans un salon vocal !")

@bot.command(name="stop", help="Arrête la musique et efface la liste d'attente")
async def stop(ctx):
    user=ctx.message.author
    for vc in voicechannel:
        if vc[0].channel == user.voice.channel:
            vc[1] = []
            vc[2] = 0
            vc[0].stop()
        else:
            await ctx.send("Vous n'êtes pas dans un salon vocal !")

@bot.command(name="next", aliases=['skip','s'], help="Passe à la musique suivante\nPS: Vous pouvez passer plusieurs musiques en indiquant le nombre de musique à sauter")
async def next(ctx, *arg):
    user=ctx.message.author
    for vc in voicechannel:
        if vc[0].channel == user.voice.channel:
            if len(arg) != 0:
                if len(vc[1]) > vc[2]+int(arg[0]):
                    vc[2] += int(arg[0]) - 1
                    vc[0].stop()
                    currentMusicName = vc[1][vc[2]+1][1]
                    await ctx.send("**Je chante🎶: **" + currentMusicName + "\n**Queue:** {}/{}".format((vc[2]+2),len(vc[1])))
                else:
                    await ctx.send("**Aïe aïe aïe !**\n`Out of Range: Le nombre entré dépasse la liste`")
            else:
                if len(vc[1]) - 1 != vc[2]:
                    vc[0].stop()
                    currentMusicName = vc[1][vc[2]+1][1]
                    await ctx.send("**Je chante🎶: **" + currentMusicName + "\n**Queue:** {}/{}".format((vc[2]+2),len(vc[1])))
                else:
                    await ctx.send("**Fin de la queue atteinte**")


@bot.command(name="back", aliases=['b'], help="Reviens à la musique précédente\nPS: Vous pouvez revenir plusieurs fois en indiquant le nombre de musique à sauter")
async def back(ctx, *arg):
    user=ctx.message.author
    for vc in voicechannel:
        if vc[0].channel == user.voice.channel:
            if len(arg) != 0:
                if vc[2] - int(arg[0]) >= 0 and vc[2] > 0:
                    vc[2] -= int(arg[0]) + 1
                    vc[0].stop()
                    currentMusicName = vc[1][vc[2]+1][1]
                    await ctx.send("**Je chante🎶: **" + currentMusicName + "\n**Queue:** {}/{}".format((vc[2]+2),len(vc[1])))
                else:
                    await ctx.send("**Aïe aïe aïe !**\nQueuedlist: Out of Range > `Le nombre entré dépasse la liste`")
            else:
                if vc[2] > 0:
                    vc[2] -= 2
                    vc[0].stop()
                    currentMusicName = vc[1][vc[2]+1][1]
                    await ctx.send("**Je chante🎶: **" + currentMusicName + "\n**Queue:** {}/{}".format((vc[2]+2),len(vc[1])))
                else:
                    await ctx.send("**Vous avez atteint le début de la liste !**")

@bot.command(name="leave", help="Permet au bot de se dégourdir les jambes (ou plutôt la bande passante")
async def leave(ctx):
    user=ctx.message.author
    for vc in voicechannel:
        if vc[0].channel == user.voice.channel:
            vc[1] = []
            vc[2] = 0
            vc[0].stop()
            vc[0].play(discord.FFmpegPCMAudio(PATH / "leave_sound.opus", executable=FFMPEG_PATH))
            await asyncio.sleep(1.5)
            await vc[0].disconnect()
            await ctx.send("Bis bald! :wave:")
            voicechannel.remove(vc)
            shutil.rmtree(PATH / ('musics/'+str(vc[0].channel.id)))
        else:
            await ctx.send("Vous n'êtes pas dans un salon vocal !")

bot.run(TOKEN)