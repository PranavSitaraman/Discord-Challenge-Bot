import discord
from discord.ext import commands
from random import randint
from csv import DictWriter, writer, reader
class Challenges(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    @commands.command(name = "add", help = "Add a new challenge")
    async def new(self, ctx, name : str, points : int):
        await ctx.send(f"{ctx.author.mention}! Enter the description for {name} below")
        def check(author):
            def inner_check(message):
                return message.author == author
            return inner_check
        try:
            desc = await self.bot.wait_for('message', check=check(ctx.author), timeout=5)
            desc = desc.content
            with open("challenges.csv",'r',newline='') as c:
                inp = [row for row in reader(c)]
            if inp[-1][0] == "id":
                cID = 1
            else:
                cID = int(inp[-1][0]) + 1
            newC = discord.Embed(title = f"New Challenge: #{cID}", type = "rich", colour = randint(0, 0xffffff))
            newC.set_author(name = ctx.author.name)
            newC.add_field(name = "Challenge Name", value = u"\u200B" + str(name), inline = False)
            newC.add_field(name = "Points Value", value = u"\u200B" + str(points), inline = False)
            newC.add_field(name = "Description", value = u"\u200B" + str(desc), inline = False)
            confirm = await ctx.send(ctx.author.mention, embed=newC)
            await confirm.add_reaction(emoji=u"\u2705")
            await confirm.add_reaction(emoji=u"\u274C")
            def check(reaction, user):
                return (user == ctx.message.author and (reaction.emoji == u"\u2705" or reaction.emoji == u"\u274C"))
            try:
                reaction, user = await self.bot.wait_for('reaction_add', check=check, timeout=5)
                if reaction.emoji == u"\u2705":
                    with open("challenges.csv",'a+',newline='') as cAdd:
                        writer = DictWriter(cAdd, fieldnames=["id","name","points","desc","finishedBy"])
                        writer.writerow({"id" : cID, "name" : name, "points" : points, "desc" : desc, "finishedBy" : ""})
                    await ctx.send(f"Success! Challenge #{cID} was added.")
                elif reaction.emoji == u"\u274C":
                    await ctx.send(f"Declined! Challenge #{cID} not added.")
            except:
                await ctx.send("Request timed out!")
        except:
            await ctx.send("Request timed out!")
    @commands.command(name = "delete", help = "Delete an existing challenge")
    async def remove(self, ctx, id : int):
        with open("challenges.csv",'r',newline='') as c:
            out = []
            for row in reader(c):
                if row[0] != str(id):
                    out.append(row)
                elif row[0] == str(id):
                    cID, name, points, desc = row[0], row[1], row[2], row[3]
        remC = discord.Embed(title = f"Removed challenge: #{cID}", type = "rich", colour = randint(0,0xffffff))
        remC.set_author(name = ctx.author.name)
        remC.add_field(name = "Challenge Name", value = u"\u200B" + str(name), inline = False)
        remC.add_field(name = "Points Value", value = u"\u200B" + str(points), inline = False)
        remC.add_field(name = "Description", value = u"\u200B" + str(desc), inline = False)
        with open("challenges.csv",'r',newline='') as c:
            dif = [row for row in reader(c)]
        for i in range(1, len(dif)):
            if int(dif[i][0]) == id:
                finishedBy = dif[i][-1].split(' ')
        output = ""
        for i in finishedBy:
            try:
                p = await self.bot.fetch_user(i)
                output += p.mention + " "
            except:
                pass
        remC.add_field(name = "Completed", value = u"\u200B" + str(output), inline = False)
        confirm = await ctx.send(ctx.author.mention, embed=remC)
        await confirm.add_reaction(emoji=u"\u2705")
        await confirm.add_reaction(emoji=u"\u274C")
        def check(reaction, user):
            return (user == ctx.message.author and (reaction.emoji == u"\u2705" or reaction.emoji == u"\u274C"))
        try:
            reaction, user = await self.bot.wait_for('reaction_add', check=check, timeout=5)
            if reaction.emoji == u"\u2705":
                with open("challenges.csv",'w',newline='') as c: [writer(c).writerow(row) for row in out]
                await ctx.send(f"Success! Challenge #{cID} removed.")
            elif reaction.emoji == u"\u274C":
                await ctx.send(f"Declined! Challenge #{cID} not removed.")
        except:
            await ctx.send("Request timed out!")
    @commands.command(name = "complete", help = "Mark a challenge complete for user")
    async def finished(self, ctx, user : discord.User, id : int):
        with open("challenges.csv",'r',newline='') as c:
            out = [row for row in reader(c)]
        for i in range(1, len(out)):
            if int(out[i][0]) == id:
                finishedBy = out[i][-1].split(' ')
                index = i
        if str(user.id) in finishedBy:
            p = await self.bot.fetch_user(user.id)
            await ctx.send(f"{p.mention} has already completed challenge #{id}")
        else:
            await ctx.message.add_reaction(emoji=u"\u2705")
            await ctx.message.add_reaction(emoji=u"\u274C")
            def check(reaction, person): return (person == ctx.message.author and (reaction.emoji == u"\u2705" or reaction.emoji == u"\u274C"))
            try:
                reaction, person = await self.bot.wait_for('reaction_add', check=check, timeout=5)
                if reaction.emoji == u"\u2705":
                    finishedBy.append(str(user.id))
                    out[index][-1] = ' '.join(finishedBy)
                    with open("challenges.csv",'w',newline='') as w:
                        writer(w).writerows(out)
                    with open("points.csv",'r',newline='') as r:
                        stats = [row for row in reader(r)]
                    for stat in stats:
                        if stat[0] == str(user.id):
                            stat[1] = int(stat[1]) + int(out[index][2])
                    with open("points.csv",'w',newline='') as w:
                        writer(w).writerows(stats)
                    p = await self.bot.fetch_user(int(user.id))
                    await ctx.send(f"Congrats on completing challenge #{id}, {p.mention}!")
                elif reaction.emoji == u"\u274C":
                    await ctx.send(f"Declined! Challenge #{id} not completed.")
            except:
                await ctx.send("Request timed out!")
    @commands.command(name = "incomplete", help = "Undo completed challenge for user")
    async def subtract(self, ctx, user : discord.User, id : int):
        with open("challenges.csv",'r',newline='') as c:
            out = [row for row in reader(c)]
        for i in range(1, len(out)):
            if int(out[i][0]) == id:
                finishedBy = out[i][-1].split(' ')
                index = i
        if str(user.id) not in finishedBy:
            p = await self.bot.fetch_user(user.id)
            await ctx.send(f"{p.mention} has not completed challenge #{id}")
        else:
            await ctx.message.add_reaction(emoji=u"\u2705")
            await ctx.message.add_reaction(emoji=u"\u274C")
            def check(reaction, person):
                return (person == ctx.message.author and (reaction.emoji == u"\u2705" or reaction.emoji == u"\u274C"))
            try:
                reaction, person = await self.bot.wait_for('reaction_add', check=check, timeout=5)
                if reaction.emoji == u"\u2705":
                    finishedBy.remove(str(user.id))
                    out[index][-1] = ' '.join(finishedBy)
                    with open("challenges.csv",'w',newline='') as w:
                        writer(w).writerows(out)
                    with open("points.csv",'r',newline='') as r:
                        stats = [row for row in reader(r)]
                    for stat in stats:
                        if stat[0] == str(user.id):
                            stat[1] = int(stat[1]) - int(out[index][2])
                    with open("points.csv",'w',newline='') as w:
                        writer(w).writerows(stats)
                    p = await self.bot.fetch_user(user.id)
                    await ctx.send(f"Sucks. It seems {p.mention} didn't do challenge #{id}.")
                elif reaction.emoji == u"\u274C":
                    await ctx.send(f"Declined! Challenge #{id} still marked complete.")
            except:
                await ctx.send("Request timed out!")