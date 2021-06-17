import discord
import os
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

client = commands.Bot(command_prefix='!')


# Discord.py docs can be found here https://discordpy.readthedocs.io/
@client.event
async def on_ready():
    for guild in client.guilds:
        if guild.name == GUILD:
            break

    print(
        f'{client.user} is connected to the following guild:\n'
        f'{guild.name}(id: {guild.id})'
    )
    await client.change_presence(activity=discord.Game('gumpin\' bubbies'))


for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        client.load_extension(f'cogs.{filename[:-3]}')
        print(f'Loaded {filename[:-3]}')

        
@client.event
async def passive_votes(ctx):
    # PASSIVE: auto-react meme-off/hot-takes
    if (ctx.channel.name == "meme-off") or (ctx.channel.name == "hot-takes") \
            and (ctx.author.id != 785635869771563018):
        # add reactions
        await ctx.add_reaction("updoot")
        await ctx.add_reaction("downdoot")
        

# announce when member joins
@client.event
async def on_member_join(member):
    print(f'{member} has joined the server.')


@client.event
async def on_member_remove(member):
    print(f'{member} has left the server.')


# load cogs
@client.command()
async def load(ctx, extension):
    client.load_extension(f'cogs.{extension}')


# unload cogs
@client.command()
async def unload(ctx, extension):
    client.unload_extension(f'cogs.{extension}')


@client.command()
async def reload(ctx, extension):
    client.unload_extension(f'cogs.{extension}')
    client.load_extension(f'cogs.{extension}')
    await ctx.send(f'{extension} loaded')


@client.command()
@commands.has_role("role doesn't exist")
async def clear(ctx, amount):
    await ctx.channel.purge(limit=amount)


client.run(TOKEN)
