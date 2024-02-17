import discord
import datetime as DT
from enum import Enum
import re

bot = discord.Bot()


class Departments(str, Enum):
    BCSO = "BCSO"
    LSPD = "LSPD"
    SAST = "SAST"

@bot.event
async def on_ready():
    print(f"We have logged in as {bot.user}")

@bot.slash_command(guild_ids=["99999999999999999999"])
async def ondutyhours(ctx, steam_user: str):
    print(steam_user)
    totalMinutes = 0
    today = DT.datetime.now()
    week_ago = today - DT.timedelta(days=today.weekday())
    week_ago = week_ago.replace(hour=0, minute=0, second=0)
    print(week_ago)

    guild = bot.get_guild(99999999999999999999)
    channel = guild.get_channel(99999999999999999999)

    totalHours = 0
    totalMinutes = 0
    embedList = []

    async for msg in channel.history(limit=200, after=week_ago):
        for embed in msg.embeds:
                if steam_user in embed.title:
                    embedList.append(embed)
    
    if embedList:
        for embed in embedList:
            if "off duty" in embed.title:
                        embedFooter = embed.footer.text
                        embedFooter = embedFooter.replace("Duration: ", "")
                        embedFooter = embedFooter.replace("minutes", "")
                        totalMinutes += int(embedFooter)
                        totalHours = round(totalMinutes/60, 2)

        userEmbed = discord.Embed(title=f"On Duty Hours for User: {steam_user}", color=discord.Colour.dark_blue())
        userEmbed.description = f"Time spent on duty: {totalMinutes} minutes({totalHours} hours) on duty this week."
        userEmbed.set_footer(text=f"{week_ago.date()} to {DT.datetime.today().date()}")
        
        await ctx.send_response(embed=userEmbed)
    else:
        await ctx.send_response(f"User: {steam_user} does not exist, or has not gone on duty in a week.")



@bot.slash_command(guild_ids=["99999999999999999999"])
async def officer_list(ctx, department: Departments):
    totalMinutes = 0
    today = DT.datetime.now()
    week_ago = today - DT.timedelta(days=today.weekday())
    week_ago = week_ago.replace(hour=0, minute=0, second=0)

    guild = bot.get_guild(99999999999999999999)
    channel = guild.get_channel(99999999999999999999)

    totalHours = 0
    totalMinutes = 0
    embedList = []
    officers = {}

    async for msg in channel.history(limit=200, after=week_ago):
        for embed in msg.embeds:
                if department in embed.description:
                    embedList.append(embed)
    
    if embedList:
        for embed in embedList:
            if "off duty" in embed.title:
                        embedFooter = embed.footer.text
                        embedFooter = embedFooter.replace("Duration: ", "")
                        embedFooter = embedFooter.replace("minutes", "")

                        embedTitle = embed.title
                        embedTitle = embedTitle.replace("Player ", "")
                        embedTitle = embedTitle.replace(" is now off duty", "")
                        embedTitle = embedTitle.replace("**", "")
                        embedTitle = re.sub("\A\s", "", embedTitle)
                        playerName = re.sub(r"(\[.....\] )", "", embedTitle)

                        totalMinutes += int(embedFooter)
                        totalHours = round(totalMinutes/60, 2)

                        previousHours = officers.get(playerName)

                        if previousHours is None:
                            previousHours = 0
                        officers.update({playerName: round(previousHours + totalHours, 2)})
            totalHours = 0
            totalMinutes = 0
    
    officerEmbed = discord.Embed(title=f"{department} Members for the week {week_ago.date()} to {DT.datetime.today().date()}", color=discord.Colour.dark_blue())
    for key in officers:
        officerEmbed.add_field(name=key, value=officers[key])

    await ctx.send_response(embed=officerEmbed)


bot.run("MTExNDc2NTE5MTE2NzYyNzM0Ng.G6a23u.lwfMEgFx69AIO_fUHE_i2XaofgIpf_30WeHqWI")
