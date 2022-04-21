import discord
from discord.ext import commands
from random import randint
from csv import reader
from utils import *
class View(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    @commands.command(name = "challenges", help = "View available challenges")
    async def challenges(self, ctx):
        with open("challenges.csv",'r',newline='') as c:
            cS = [[row[0],row[1],row[2]] for row in reader(c)]
        cS.pop(0)
        active = discord.Embed(title = "Active Challenges", type = "rich", colour = randint(0, 0xffffff))
        active.set_author(name = ctx.author.name)
        for c in cS:
            active.add_field(name = int2Emoji(c[0]), value = f"Name: {c[1]}\nPoints: {c[2]}", inline = False)
        await ctx.send(ctx.author.mention, embed=active)
    @commands.command(name = "details", help = "View details of a challenge")
    async def details(self, ctx, id : int):
        with open("challenges.csv",'r') as c:
            cS = [row for row in reader(c) if row[0] == str(id)]
            cS = cS[0]
        det = discord.Embed(title = f"Details: Challenge #{cS[0]}", type = "rich", colour = randint(0, 0xffffff))
        det.set_author(name = ctx.author.name)
        det.add_field(name = "Name", value = u"\u200B" + str(cS[1]), inline = False)
        det.add_field(name = "Points", value = u"\u200B" + str(cS[2]), inline = False)
        det.add_field(name = "Description", value = u"\u200B" + str(cS[3]), inline = False)
        with open("challenges.csv",'r',newline='') as c:
            out = [row for row in reader(c)]
        for i in range(1, len(out)):
            if int(out[i][0]) == id:
                finishedBy = out[i][-1].split(' ')
        output = ""
        for i in finishedBy:
            try:
                p = await self.bot.fetch_user(i)
                output += p.mention + " "
            except:
                pass
        det.add_field(name = "Completed", value = u"\u200B" + str(output), inline = False)
        await ctx.send(ctx.author.mention, embed=det)
    @commands.command(name = "leaderboard", help = "View the current leaderboard")
    async def leaderboard(self, ctx):
        leaderSort('points.csv')
        with open("points.csv",'r') as points:
            stats = [row for row in reader(points)]
        standings = discord.Embed(title = "Live Standings", type = "rich", colour = randint(0, 0xffffff))
        standings.set_author(name = ctx.author.name)
        for rank in range(1, len(stats)):
            try:
                p = await self.bot.fetch_user(int(stats[rank][0]))
                standings.add_field(name = int2Emoji(rank), value = f"{p.name}: {stats[rank][1]} points", inline = False)
            except:
                pass
        await ctx.send(ctx.message.author.mention, embed=standings)