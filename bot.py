import discord
import os
import sqlite3
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

#strike db info
conn = sqlite3.connect('strikers.db')
cur = conn.cursor()
command1 = """CREATE TABLE IF NOT EXISTS
strikers (name TEXT, strikes INTEGER)"""
cur.execute(command1)
conn.commit()

# addstrike command
@client.command()
@commands.has_role("striker")
async def addstrike(ctx, person):
    with conn:
        cur.execute("SELECT name FROM strikers")
        name_tuple = cur.fetchall()
        names = list(name_tuple)
        good_names = " ".join(map(str, names)).replace(')', '').replace('(', '').replace(',', '').replace("'", '')
        if person.lower() in good_names:
            get_old_strikes = f"SELECT strikes " \
                              f"FROM strikers " \
                              f"WHERE name ='{person.lower()}'"
            cur.execute(get_old_strikes)
            old_strikes = cur.fetchone()
            list_strikes = list(old_strikes)
            int_strikes = " ".join(map(str, list_strikes)).replace(')', '').replace('(', '').replace(',', '').replace("'", '')
            new_strikes = int(int_strikes) + 1
            cur.execute(f"UPDATE strikers "
                        f"SET strikes='{new_strikes}'"
                        f"WHERE name='{person.lower()}'")
            await ctx.send(f'{person.title()} now has {new_strikes} strikes!')
        else:
            cur.execute(f"INSERT INTO strikers(name, strikes) "
                        f"VALUES ('{person.lower()}', 1)")
            await ctx.send(f'{person.title()} now has 1 strike!')
#removes strike from person
@client.command(alises=['rmstrike'])
@commands.has_role("striker")
async def rm_strike(ctx, person):
    with conn:
        cur.execute("SELECT name FROM strikers")
        name_tuple = cur.fetchall()
        names = list(name_tuple)
        good_names = " ".join(map(str, names)).replace(')', '').replace('(', '').replace(',', '').replace("'", '')
        cur.execute(f"SELECT strikes FROM strikers WHERE name='{person.lower()}'")
        strike_tuple = cur.fetchone()
        strike_count = " ".join(map(str, strike_tuple)).replace(')', '').replace('(', '').replace(',', '').replace("'", '')
        if person.lower() in good_names and strike_count != '0':
            get_old_strikes = f"SELECT strikes " \
                              f"FROM strikers " \
                              f"WHERE name ='{person.lower()}'"
            cur.execute(get_old_strikes)
            old_strikes = cur.fetchone()
            list_strikes = list(old_strikes)
            int_strikes = " ".join(map(str, list_strikes)).replace(')', '').replace('(', '').replace(',', '').replace("'", '')
            new_strikes = int(int_strikes) - 1
            cur.execute(f"UPDATE strikers "
                        f"SET strikes='{new_strikes}'"
                        f"WHERE name='{person.lower()}'")
            await ctx.send(f'{person.title()} now has {new_strikes} strikes!')
        else:
            await ctx.send(f'{person.title()} does not have any strikes to be removed!')

# list strikes of person
@client.command()
async def strikes(ctx, person):
    with conn:
        cur.execute("SELECT name FROM strikers")
        name_tuple = cur.fetchall()
        names = list(name_tuple)
        good_names = " ".join(map(str, names)).replace(')', '').replace('(', '').replace(',', '').replace("'", '')
        if person.lower() in good_names:
            cur.execute(f"SELECT strikes FROM strikers WHERE name='{person.lower()}'")
            strike_tuple = cur.fetchone()
            strike_count = " ".join(map(str, strike_tuple)).replace(')', '').replace('(', '').replace(',', '').replace(
                "'", '')
            await ctx.send(f"{person.title()} has {strike_count} strikes!")
        else:
            await ctx.send(f"{person.title()} has 0 strikes!")



#announce when member joins
@client.event
async def on_member_join(member):
    print(f'{member} has joined the server.')


@client.event
async def on_member_remove(member):
    print(f'{member} has left the server.')

# ping command - reports bot latency
@client.command()
@commands.cooldown(1, 30, commands.BucketType.guild)
async def ping(ctx):
    if commands.errors.CommandOnCooldown:
        await ctx.channel.purge(limit=1)
        await ctx.send(f'Pong! Bot latency is currently {round(client.latency * 1000)}ms')
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
