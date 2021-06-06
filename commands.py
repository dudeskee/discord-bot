from bot import client
from discord.ext import commands
import sqlite3

conn = sqlite3.connect('./strikers.db')
cur = conn.cursor()
command1 = """CREATE TABLE IF NOT EXISTS
strikers (name TEXT, strikes INTEGER)"""
cur.execute(command1)
conn.commit()


class Commands(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print('Commands are ready.')

    # ping command - reports bot latency
    @commands.command()
    @commands.cooldown(1, 30, commands.BucketType.guild)
    async def ping(self, ctx):
        if commands.errors.CommandOnCooldown:
            await ctx.channel.purge(limit=1)
            await ctx.send(f'Pong! Bot latency is currently {round(client.latency * 1000)}ms')
        else:
            await ctx.send('nope')

    # strike command
    @commands.command()
    @commands.has_role("striker")
    async def addstrike(self, ctx, person):
        with conn:
            cur.execute("SELECT name FROM strikers")
            name_tuple = cur.fetchall()
            good_names = list(row[0] for row in name_tuple)
            if person.lower() in good_names:
                get_old_strikes = f"SELECT strikes " \
                                  f"FROM strikers " \
                                  f"WHERE name ='{person.lower()}'"
                cur.execute(get_old_strikes)
                old_strikes = cur.fetchone()
                new_strikes = int(old_strikes[0]) + 1
                cur.execute(f"UPDATE strikers "
                            f"SET strikes='{new_strikes}'"
                            f"WHERE name='{person.lower()}'")
                await ctx.send(f'{person.title()} now has {new_strikes} strikes!')
            else:
                cur.execute(f"INSERT INTO strikers(name, strikes) "
                            f"VALUES ('{person.lower()}', 1)")
                await ctx.send(f'{person.title()} now has 1 strike!')

    @commands.command(aliases=['rmstrike'])
    @commands.has_role("striker")
    async def rm_strike(self, ctx, person):
        with conn:
            cur.execute("SELECT name FROM strikers")
            name_tuple = cur.fetchall()
            good_names = list(row[0] for row in name_tuple)
            cur.execute(f"SELECT strikes FROM strikers WHERE name='{person.lower()}'")
            strike_tuple = cur.fetchone()
            strike_count = strike_tuple[0]
            if person.lower() in good_names and strike_count != '0':
                get_old_strikes = f"SELECT strikes " \
                                  f"FROM strikers " \
                                  f"WHERE name ='{person.lower()}'"
                cur.execute(get_old_strikes)
                old_strikes = cur.fetchone()
                new_strikes = int(old_strikes[0]) - 1
                cur.execute(f"UPDATE strikers "
                            f"SET strikes='{new_strikes}'"
                            f"WHERE name='{person.lower()}'")
                await ctx.send(f'{person.title()} now has {new_strikes} strikes!')
            else:
                await ctx.send(f'{person.title()} does not have any strikes to be removed!')

    @commands.command(aliases=['sc'])
    async def strikecheck(self, ctx):
        with conn:
            cur.execute("SELECT * FROM strikers")
            names = list(cur.fetchall())
            await ctx.send("Strikes are as follows:")
            for person, strikes in names:
                await ctx.send(f"{person} - {strikes}")

    @commands.command(aliases=['bigvote', 'numvote', 'nv'])
    async def add_big_vote(self, ctx, amnt, prge=1):
        msg = await ctx.channel.history(limit=3).flatten()
        emoji_numbers = ["1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣", "6️⃣", "7️⃣", "8️⃣", "9️⃣", "0️⃣"]
        allow_amounts = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10"]
        if amnt in allow_amounts:
            await ctx.channel.purge(limit=prge)
            amount = int(amnt)
            for counter in range(amount):
                await msg[1].add_reaction(emoji_numbers[counter])
        elif amnt not in allow_amounts:
            await ctx.send(f'{amnt} is an invalid input. Single numbers, 1 to 10.')

    @commands.command(aliases=['addvote', 'vote', 'doots', 'doot'])
    async def add_vote(self, ctx, amount=1):
        # get history
        messages = await ctx.channel.history(limit=3).flatten()
        # delete command
        await ctx.channel.purge(limit=amount)
        # add reactions
        await messages[1].add_reaction("updoot:692862052599070720")  # 692862052599070720
        await messages[1].add_reaction("downdoot:692862024241250334")  # 692862024241250334


def setup(bot):
    bot.add_cog(Commands(bot))
