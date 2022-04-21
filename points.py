import discord
from discord.ext import commands
from csv import writer, reader
class Points(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    @commands.command(name = "give", help = "Give points to a user")
    async def give(self, ctx, user : discord.User, points : int):
        await ctx.message.add_reaction(emoji=u"\u2705")
        await ctx.message.add_reaction(emoji=u"\u274C")
        def check(reaction, user):
            return (user == ctx.message.author and (reaction.emoji == u"\u2705" or reaction.emoji == u"\u274C"))
        try:
            reaction, user = await self.bot.wait_for('reaction_add', check=check, timeout=5)
            if reaction.emoji == u"\u2705":
                with open("points.csv",'r',newline='') as c:
                    out = [row for row in reader(c)]
                for i in range(1, len(out)):
                    if out[i][0] == str(user.id):
                        out[i][1] = str(int(out[i][1]) + points)
                with open("points.csv",'w',newline='') as c:
                    [writer(c).writerow(row) for row in out]
                await ctx.send(f"Success! Points were given.")
            elif reaction.emoji == u"\u274C":
                await ctx.send(f"Declined! Points not given.")
        except:
            await ctx.send("Request timed out!")
    @commands.command(name = "take", help = "Take points from a user")
    async def take(self, ctx, user : discord.User, points : int):
        await ctx.message.add_reaction(emoji=u"\u2705")
        await ctx.message.add_reaction(emoji=u"\u274C")
        def check(reaction, user):
            return (user == ctx.message.author and (reaction.emoji == u"\u2705" or reaction.emoji == u"\u274C"))
        try:
            reaction, user = await self.bot.wait_for('reaction_add', check=check, timeout=5)
            if reaction.emoji == u"\u2705":
                with open("points.csv",'r',newline='') as c:
                    out = [row for row in reader(c)]
                for i in range(1, len(out)):
                    if out[i][0] == str(user.id):
                        out[i][1] = str(int(out[i][1]) - points)
                with open("points.csv",'w',newline='') as c:
                    [writer(c).writerow(row) for row in out]
                await ctx.send(f"Success! Points were taken.")
            elif reaction.emoji == u"\u274C":
                await ctx.send(f"Declined! Points not taken.")
        except:
            await ctx.send("Request timed out!")