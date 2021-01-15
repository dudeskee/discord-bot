import discord
import os
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

client = commands.Bot(command_prefix='!')


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


# For future use with cogs - remove # when cogs configured
#for filename in os.listdir('./cogs'):
#    if filename.endswith('.py'):
#        client.load_extension(f'cogs.{filename[:-3]}')


# ping command - reports bot latency
@client.command()
@commands.cooldown(1, 30, commands.BucketType.guild)
async def ping(ctx):
    if commands.errors.CommandOnCooldown:
        await ctx.channel.purge(limit=1)
        await ctx.send(f'Pong! {round(client.latency * 1000)}ms')
    else:
        await ctx.send('nope')


# kick command - must have punisher role
@client.command(aliases=['boot', 'punt'])
@commands.has_role("punisher")
async def kick(ctx, member : discord.Member, *, reason=None):
    await member.kick(reason=reason)
    await ctx.channel.purge(limit=1)
    await ctx.send(f'{member} was kicked for {reason}!')


# ban command - must have punisher role
@client.command()
@commands.has_role("punisher")
async def ban(ctx, member : discord.Member, *, reason=None):
    await member.ban(reason=reason)
    # delete command
    await ctx.channel.purge(limit=1)
    await ctx.send(f'{member} was banned for {reason}!')

# unban command - must have punisher role
@client.command()
@commands.has_role("punisher")
async def unban(ctx, *, member):
    await ctx.channel.purge(limit=1)
    banned_users = await ctx.guild.bans()
    member_name, member_discriminator = member.split('#')

    for ban_entry in banned_users:
        user = ban_entry.user

        if (user.name, user.discriminator) == (member_name, member_discriminator):
            await ctx.guild.unban(user)
            await ctx.send(f'Unbanned {user.mention}')
            return

# ban taylor command - Anyone can use it
@client.command()
async def fuckTaylor(ctx, member = discord.Member):
    if(member.id != 396826774887071744):
        "Target is not taylor. Please ban taylor stykes."
        return

    reason = "You have been fucked on Taylor"
    await member.ban(reason)
    # delete command
    await ctx.channel.purge(limit=1)
    await ctx.send(f'{member} was banned for {reason}!')


@client.command(aliases=['addvote', 'vote', 'doots', 'doot'])
async def add_vote(ctx, amount=1):
    # get history
    messages = await ctx.channel.history(limit=3).flatten()
    # delete command
    await ctx.channel.purge(limit=amount)
    # add reactions
    await messages[1].add_reaction("updoot:692862052599070720")  # 692862052599070720
    await messages[1].add_reaction("downdoot:692862024241250334")  # 692862024241250334


@client.command()
@commands.has_role("role doesn't exist")
async def clear(ctx, amount):
    await ctx.channel.purge(limit=amount)


@client.command(aliases=['bigvote', 'numvote', 'nv'])
async def add_big_vote(ctx, amount: int, prge=1):
    msg = await ctx.channel.history(limit=3).flatten()
    if amount == 1:
        await ctx.channel.purge(limit=prge)
        await msg[1].add_reaction("1️⃣")

    elif amount == 2:
        await ctx.channel.purge(limit=prge)
        await msg[1].add_reaction("1️⃣")
        await msg[1].add_reaction("2️⃣")

    elif amount == 3:
        await ctx.channel.purge(limit=prge)
        await msg[1].add_reaction("1️⃣")
        await msg[1].add_reaction("2️⃣")
        await msg[1].add_reaction("3️⃣")

    elif amount == 4:
        await ctx.channel.purge(limit=prge)
        await msg[1].add_reaction("1️⃣")
        await msg[1].add_reaction("2️⃣")
        await msg[1].add_reaction("3️⃣")
        await msg[1].add_reaction("4️⃣")

    elif amount == 5:
        await ctx.channel.purge(limit=prge)
        await msg[1].add_reaction("1️⃣")
        await msg[1].add_reaction("2️⃣")
        await msg[1].add_reaction("3️⃣")
        await msg[1].add_reaction("4️⃣")
        await msg[1].add_reaction("5️⃣")

    elif amount == 6:
        await ctx.channel.purge(limit=prge)
        await msg[1].add_reaction("1️⃣")
        await msg[1].add_reaction("2️⃣")
        await msg[1].add_reaction("3️⃣")
        await msg[1].add_reaction("4️⃣")
        await msg[1].add_reaction("5️⃣")
        await msg[1].add_reaction("6️⃣")

    elif amount == 7:
        await ctx.channel.purge(limit=prge)
        await msg[1].add_reaction("1️⃣")
        await msg[1].add_reaction("2️⃣")
        await msg[1].add_reaction("3️⃣")
        await msg[1].add_reaction("4️⃣")
        await msg[1].add_reaction("5️⃣")
        await msg[1].add_reaction("6️⃣")
        await msg[1].add_reaction("7️⃣")

    elif amount == 8:
        await ctx.channel.purge(limit=prge)
        await msg[1].add_reaction("1️⃣")
        await msg[1].add_reaction("2️⃣")
        await msg[1].add_reaction("3️⃣")
        await msg[1].add_reaction("4️⃣")
        await msg[1].add_reaction("5️⃣")
        await msg[1].add_reaction("6️⃣")
        await msg[1].add_reaction("7️⃣")
        await msg[1].add_reaction("8️⃣")

    elif amount == 9:
        await ctx.channel.purge(limit=prge)
        await msg[1].add_reaction("1️⃣")
        await msg[1].add_reaction("2️⃣")
        await msg[1].add_reaction("3️⃣")
        await msg[1].add_reaction("4️⃣")
        await msg[1].add_reaction("5️⃣")
        await msg[1].add_reaction("6️⃣")
        await msg[1].add_reaction("7️⃣")
        await msg[1].add_reaction("8️⃣")
        await msg[1].add_reaction("9️⃣")

    elif amount == 0:
        await ctx.channel.purge(limit=prge)
        await msg[1].add_reaction("1️⃣")
        await msg[1].add_reaction("2️⃣")
        await msg[1].add_reaction("3️⃣")
        await msg[1].add_reaction("4️⃣")
        await msg[1].add_reaction("5️⃣")
        await msg[1].add_reaction("6️⃣")
        await msg[1].add_reaction("7️⃣")
        await msg[1].add_reaction("8️⃣")
        await msg[1].add_reaction("9️⃣")
        await msg[1].add_reaction("0️⃣")

    else:
        await ctx.send(f'{amount} is an invalid input. Single numbers, 0 to 9.')



@client.event
async def passive_votes(ctx):
    # PASSIVE: auto-react meme-off/hot-takes
    if (ctx.channel.name == "meme-off") or (ctx.channel.name == "hot-takes") \
            and (ctx.author.id != 785635869771563018):
        # add reactions
        await ctx.add_reaction("updoot:692862052599070720")
        await ctx.add_reaction("downdoot:692862024241250334")


client.run(TOKEN)
