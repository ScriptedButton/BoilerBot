#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# BoilerBot V1.1
# Written by Cole^2

from concurrent.futures import ThreadPoolExecutor
import asyncio
import os

from discord.ext import commands
import discord

from utils import parseCourseInfo

description = "BoilerBot"
bot = commands.Bot(command_prefix='?', description=description)
token = os.getenv("BOT_TOKEN")

loop = asyncio.get_event_loop()

if token is None:
    print("Unable to retrieve data for env variable `BOT_TOKEN`. Exitting!")
    exit(0)


@bot.event
async def on_ready():
    print(f'Logged in as {bot.user} (ID: {bot.user.id})')
    print('------')


@bot.command()
async def courseinfo(ctx, subject: str, number: int):
    course = await loop.run_in_executor(
        ThreadPoolExecutor(), parseCourseInfo, subject, number
    )
    embed = discord.Embed(title=course.title,
                          description=course.description, color=0xdbce14)
    embed.add_field(name="Credit Hours",
                    value=course.credits, inline=False)
    await ctx.send(embed=embed)

bot.run(token)
