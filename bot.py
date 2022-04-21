from discord.ext import commands
from os import getenv
from dotenv import load_dotenv
from random import randint
from csv import DictWriter, writer, reader
from pandas import read_csv
from view import View
from challenges import Challenges
from points import Points
load_dotenv()
TOKEN = getenv("DISCORD_TOKEN")
GUILD = getenv("DISCORD_GUILD")
bot = commands.Bot(command_prefix = commands.when_mentioned_or('cb!'), description = "A Discord Challenge Bot for your social circles!", help_command = commands.DefaultHelpCommand(no_category = 'Basics'))
@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to {bot.guilds[0].name}!')
@bot.event
async def on_member_join(member):
    print(f'{member.name} joined!')
    await member.create_dm()
    await member.dm_channel.send(f'Hi {member.name}, get ready for challenges!')
@bot.command(name = "ready", help = "Join the challenges")
async def ready(ctx):
    await ctx.message.add_reaction(emoji=u"\u2705")
    await ctx.message.add_reaction(emoji=u"\u274C")
    def check(reaction, user):
        return (user == ctx.message.author and (reaction.emoji == u"\u2705" or reaction.emoji == u"\u274C"))
    try:
        reaction, user = await bot.wait_for('reaction_add', check=check, timeout=5)
        if reaction.emoji == u"\u2705":
            with open("points.csv",'r',newline='') as c:
                inp = [row[0] for row in reader(c)]
                if str(ctx.message.author.id) in inp:
                    await ctx.send(f"Sorry {ctx.message.author.mention}, you are already in the game!")
                else:
                    with open("points.csv", 'a+',newline='') as points:
                        writer = DictWriter(points, fieldnames=["user","points"])
                        writer.writerow({"user" : ctx.message.author.id, "points" : 0})
                    await ctx.send(f"Welcome {ctx.message.author.mention}!")
        elif reaction.emoji == u"\u274C":
            await ctx.send("Declined! Hope you join next time!")
    except:
        await ctx.send("Request timed out!")
bot.add_cog(Challenges(bot))
bot.add_cog(Points(bot))
bot.add_cog(View(bot))
bot.run(TOKEN)