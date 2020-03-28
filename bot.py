import discord
from discord.ext import commands

from requests.exceptions import HTTPError
import json
import asyncio
import aiohttp

bot = commands.Bot(command_prefix='^')


def jprint(obj):
    text = json.dumps(obj, sort_keys=True,indent=4)
    print(text)


@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')


@bot.command(name='multiply')
async def multiply(ctx, a: int, b: int):
    await ctx.send(a*b)


@bot.command(name='player', help='Find information on a user playing Risk.')
async def player(ctx, arg):
    url = ("https://collegefootballrisk.com/api/player?player=" + arg)
    async with aiohttp.ClientSession() as session:
        raw_response = await session.get(url)
        response = await raw_response.text()
        response = json.loads(response)

        embed = discord.Embed(title="Player Info", description="Information about reddit user [/u/" + arg + "](https://reddit.com/u/" + arg + ")",
                              color=0x8b03ad)
        embed.add_field(name="Team", value = response['team']['name'], inline=False)
        embed.add_field(name="MVPs", value = str(response['ratings']['mvps']), inline=False)
        embed.add_field(name="Stars", value = str(response['turns'][0]['stars']), inline=False)
        await ctx.send(embed=embed)


@bot.command(name='team')
async def team(ctx, *, arg):
    url = ("https://collegefootballrisk.com/api/stats/team?team=" + arg)
    teamUrl = "https://api.collegefootballdata.com/teams/fbs?year=2020"
    async with aiohttp.ClientSession() as session:
        raw_response = await session.get(url)
        response = await raw_response.text()
        response = json.loads(response)

        team_raw_response = await session.get(teamUrl)
        team_response = await team_raw_response.text()
        team_response = json.loads(team_response)
        jprint(team_response)

        embed = discord.Embed(title="Team Info",
                              description="Team info",
                              color=0x8b03ad)
        embed.add_field(name="Team", value=response['team'], inline=False)
        embed.add_field(name="Players", value=str(response['players']), inline=False)
        embed.add_field(name="Mercs", value=str(response['mercs']), inline=False)
        embed.add_field(name="Stars", value=str(response['stars']), inline=False)
        embed.add_field(name="Territories", value=str(response['territories']), inline=False)
        await ctx.send(embed=embed)


@bot.command(name='quit')
async def quit(ctx):
    await ctx.send("Good bye world! 😭")
    print(f"User `{ctx.author}` turned off the bot.")
    await bot.logout()


@bot.event
async def on_error(event, *args, **kwargs):
    with open('err.log', 'a') as f:
        if event == 'on_message':
            f.write(f'Unhandled message: {args[0]}\n')
        else:
            raise

bot.run('NjMxMDA0Mzc0ODU2MTA2MDA0.Xnz08Q.RfKN-YxSwd7Yy5u08gjlpu40f-U')