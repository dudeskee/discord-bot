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

    if message.content == "!addVote":
        # get history
        messages = await message.channel.history(limit=3).flatten()

        # add reactions
        await messages[1].add_reaction("updoot:692862052599070720")
        await messages[1].add_reaction("downdoot:692862024241250334")

        # delete command
        await message.delete()


client.run(TOKEN)
