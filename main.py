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



@bot.command(name="courseinfo")
async def course_info(ctx, subject: str, number: int):
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
    emojis = ['🥓', '🍕', '🍔']

    if ret is None:
        await ctx.send(f"Key `{opt}` does not exist in menus.")
    else:
        # TODO: Handle reactions.`.
        menu = await loop.run_in_executor(ThreadPoolExecutor(), get_menu, ret)
        output = "\n".join([str(x.Name) for x in menu.Meals])
        embed = discord.Embed(title=f"Dining Info [{ret}]",
                              description=output, color=0xdbce14)
        msg = await ctx.send(embed=embed)
        for emoji in emojis:
            await msg.add_reaction(emoji)


bot.run(token)
