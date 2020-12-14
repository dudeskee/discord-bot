# bot.py
import os

import discord
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

client = discord.Client()


@client.event
async def on_ready():
    for guild in client.guilds:
        if guild.name == GUILD:
            break

    print(
        f'{client.user} is connected to the following guild:\n'
        f'{guild.name}(id: {guild.id})'
    )


@client.event
async def on_message(message):

    # COMMAND: !addVote
    if message.content == "!addVote":
        # get history
        messages = await message.channel.history(limit=3).flatten()

        # add reactions
        await messages[1].add_reaction("updoot:692862052599070720")
        await messages[1].add_reaction("downdoot:692862024241250334")

        # delete command
        await message.delete()

    # COMMAND: !addBigVote##
    if "!addBigVote" in message.content:
        # get history
        messages = await message.channel.history(limit=3).flatten()

        # add reactions
        if message.content[-1] == "1":
            await messages[1].add_reaction("0️⃣")
        elif message.content[-1] == "2":
            await messages[1].add_reaction("0️⃣")
            await messages[1].add_reaction("1️⃣")
        elif message.content[-1] == "3":
            await messages[1].add_reaction("0️⃣")
            await messages[1].add_reaction("1️⃣")
            await messages[1].add_reaction("2️⃣")
        elif message.content[-1] == "4":
            await messages[1].add_reaction("0️⃣")
            await messages[1].add_reaction("1️⃣")
            await messages[1].add_reaction("2️⃣")
            await messages[1].add_reaction("3️⃣")
        elif message.content[-1] == "5":
            await messages[1].add_reaction("0️⃣")
            await messages[1].add_reaction("1️⃣")
            await messages[1].add_reaction("2️⃣")
            await messages[1].add_reaction("3️⃣")
            await messages[1].add_reaction("4️⃣")
        elif message.content[-1] == "6":
            await messages[1].add_reaction("0️⃣")
            await messages[1].add_reaction("1️⃣")
            await messages[1].add_reaction("2️⃣")
            await messages[1].add_reaction("3️⃣")
            await messages[1].add_reaction("4️⃣")
            await messages[1].add_reaction("5️⃣")
        elif message.content[-1] == "7":
            await messages[1].add_reaction("0️⃣")
            await messages[1].add_reaction("1️⃣")
            await messages[1].add_reaction("2️⃣")
            await messages[1].add_reaction("3️⃣")
            await messages[1].add_reaction("4️⃣")
            await messages[1].add_reaction("5️⃣")
            await messages[1].add_reaction("6️⃣")
        elif message.content[-1] == "8":
            await messages[1].add_reaction("0️⃣")
            await messages[1].add_reaction("1️⃣")
            await messages[1].add_reaction("2️⃣")
            await messages[1].add_reaction("3️⃣")
            await messages[1].add_reaction("4️⃣")
            await messages[1].add_reaction("5️⃣")
            await messages[1].add_reaction("6️⃣")
            await messages[1].add_reaction("7️⃣")
        elif message.content[-1] == "9":
            await messages[1].add_reaction("0️⃣")
            await messages[1].add_reaction("1️⃣")
            await messages[1].add_reaction("2️⃣")
            await messages[1].add_reaction("3️⃣")
            await messages[1].add_reaction("4️⃣")
            await messages[1].add_reaction("5️⃣")
            await messages[1].add_reaction("6️⃣")
            await messages[1].add_reaction("7️⃣")
            await messages[1].add_reaction("8️⃣")
        elif message.content[-1] == "0":
            await messages[1].add_reaction("0️⃣")
            await messages[1].add_reaction("1️⃣")
            await messages[1].add_reaction("2️⃣")
            await messages[1].add_reaction("3️⃣")
            await messages[1].add_reaction("4️⃣")
            await messages[1].add_reaction("5️⃣")
            await messages[1].add_reaction("6️⃣")
            await messages[1].add_reaction("7️⃣")
            await messages[1].add_reaction("8️⃣")
            await messages[1].add_reaction("9️⃣")
        else:
            await message.channel.send("Invalid input")

        # delete command
        await message.delete()

    # PASSIVE: auto-react meme-off/hot-takes
    if (message.channel.name == "meme-off") or (message.channel.name == "hot-takes") \
            and (message.author.id != 785635869771563018):
        # add reactions
        await message.add_reaction("updoot:692862052599070720")
        await message.add_reaction("downdoot:692862024241250334")


client.run(TOKEN)
