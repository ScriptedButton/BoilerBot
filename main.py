#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# BoilerBot V1.1
# Written by Cole^2

import asyncio
import os
from concurrent.futures import ThreadPoolExecutor
from typing import Dict

import discord
from discord.ext import commands

from utils import parse_course_info, get_menus, get_menu

description = "BoilerBot"
bot = commands.Bot(command_prefix='?', description=description)
token = os.getenv("BOT_TOKEN")

loop = asyncio.get_event_loop()

if token is None:
    print("Unable to retrieve data for env variable `BOT_TOKEN`. Exitting!")
    exit(0)

_menus: Dict[int, str] = {}


@bot.event
async def on_ready():
    print(f'Logged in as {bot.user} (ID: {bot.user.id})')
    print('------')


@bot.command()
async def courseinfo(ctx, subject: str, number: int):
    course = await loop.run_in_executor(
        ThreadPoolExecutor(), parse_course_info, subject, number
    )
    embed = discord.Embed(title=course.title,
                          description=course.description, color=0xdbce14)
    embed.add_field(name="Credit Hours",
                    value=course.credits, inline=False)
    await ctx.send(embed=embed)


@bot.command()
async def menus(ctx):
    menus = await loop.run_in_executor(ThreadPoolExecutor(), get_menus)
    output = ""

    for index, location in enumerate(menus, 1):
        output += f"[{index}] {location.name}\n"
        _menus[index] = location.name

    embed = discord.Embed(title="Dining Offerings",
                          description=output, color=0xdbce14)
    await ctx.send(embed=embed)


@bot.command()
async def menu(ctx, opt: int):
    ret = _menus.get(opt, None)

    if ret is None:
        await ctx.send(f"Key `{opt}` does not exist in menus.")
    else:
        # TODO: get data from `ret`.
        data = await loop.run_in_executor(ThreadPoolExecutor(), get_menu, ret)
        embed = discord.Embed(title=f"Dining Info [{ret}]",
                              description=data, color=0xdbce14)
        await ctx.send(embed=embed)


bot.run(token)
