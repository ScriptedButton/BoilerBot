#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# BoilerBot V2.0
# Written by Cole^2

import asyncio
import os
import re
import itertools
from concurrent.futures import ThreadPoolExecutor

import ratemyprofessor
import discord
from discord.ext import commands


from bot_classes import MenuDropdownView
from utils import parse_course_info

DESCRIPTION = "BoilerBot"
PURDUE_COLOR_CODE = 0xCEB888
ERROR_OCCURRED_TITLE = "An Error Occurred"

intents = discord.Intents.default()

bot = commands.Bot(
    command_prefix='$',
    description=DESCRIPTION,
    status="Boiler Up! Hammer Down!",
    help_command=None,
    intents=intents
)

token = os.getenv("BOT_TOKEN")

loop = asyncio.get_event_loop()

if token is None:
    print("Unable to retrieve data for env variable `BOT_TOKEN`. Exiting!")
    exit(0)


@bot.event
async def on_ready():
    print(f'Logged in as {bot.user} (ID: {bot.user.id})')
    print('------')
    bot_status = discord.Streaming(name="Boiler Up! Hammer Down!", url="https://purdue.edu")
    await bot.change_presence(activity=bot_status)


@bot.command()
async def help(ctx):
    desc = "[1] ?courseinfo [subject] [number] - Gives you course information." \
           "\n[2] ?menus - Pulls dining menus from Purdue." \
           "\n[3] ?rateprof [name] - Gives details about a specific professor."
    help_embed = discord.Embed(title="[BoilerBot Documentation]",
                               description=desc,
                               color=PURDUE_COLOR_CODE)
    help_embed.set_footer(text="Written by Cole^2 | BoilerBot 2021")
    await ctx.send(embed=help_embed)


@bot.command()
async def menus(ctx):
    import purdue.models
    try:
        dining = purdue.models.Dining()
        await dining.load()
        locations = dining.locations
        locations_embed = discord.Embed(
            title="[All Locations]",
            description="\n".join([str(x.name) for x in locations]),
            color=PURDUE_COLOR_CODE
        )
        menu_dropdown_view_obj = MenuDropdownView(ctx.message.author.id, dining)
        await ctx.send(embed=locations_embed, view=menu_dropdown_view_obj)
    except Exception as e:
        error_embed = discord.Embed(
            title=ERROR_OCCURRED_TITLE,
            description=f"{str(e)}\n\nThis usually means Purdue has no data on an item!",
            color=discord.Color.red())
        await ctx.send(embed=error_embed)


@bot.command(name="courseinfo")
async def course_info(ctx, subject: str, number: int = 0):
    try:
        num_string = str()
        # if (len(subject) > 4):
            # y = re.search('\d+', f"{subject}{str(number)}").group()
            # x = subject.split(str(y))
            # subject = x[0]
            # num_string = x[1]

        if (len(str(number)) < 5):
            num_string = str(number)
            num_string += "00"
        else:
            num_string = str(number)

        course = await loop.run_in_executor(
            ThreadPoolExecutor(), parse_course_info, subject, int(num_string)
        )
        embed = discord.Embed(title=course.title,
                              description=course.description, color=PURDUE_COLOR_CODE)
        embed.add_field(name="Credit Hours",
                        value=course.credits, inline=False)
        await ctx.send(embed=embed)
    except Exception as e:
        error_embed = discord.Embed(
            title=ERROR_OCCURRED_TITLE,
            description=f"**{str(e)}\n\nThis usually means Purdue has no data on an item!**",
            color=discord.Color.red()
        )
        await ctx.send(embed=error_embed)


@bot.command(name="rateprof")
async def rate_prof(ctx, *, name):
    try:
        if name.lower() == "mitch daniels":
            prof_embed = discord.Embed(
                title="[Mitch Daniels]",
                description="Literally a god among men",
                color=PURDUE_COLOR_CODE
            )
            await ctx.send(embed=prof_embed)
        else:
            purdue = await loop.run_in_executor(
                ThreadPoolExecutor(),
                ratemyprofessor.get_school_by_name,
                "Purdue"
            )

            prof = await loop.run_in_executor(
                ThreadPoolExecutor(),
                ratemyprofessor.get_professor_by_school_and_name,
                purdue,
                name
            )

            if type(prof.would_take_again) == (float or int) and prof.would_take_again > 0:
                would_take_again = f"{round(prof.would_take_again)}%"
            else:
                would_take_again = "N/A"

            desc = f"Professor Difficulty: **{prof.difficulty or None}**" \
                   f"\nProfessor Rating: **{prof.rating or None}**" \
                   f"\nNumber of Ratings: **{prof.num_ratings or None}**" \
                   f"\nDepartment: **{prof.department or None}**" \
                   f"\nWould Take Again: **{would_take_again or None}**"
            prof_embed = discord.Embed(
                title=f"[{prof.name or None}]",
                description=desc,
                color=PURDUE_COLOR_CODE
            )
            await ctx.send(embed=prof_embed)
    except Exception:
        error_embed = discord.Embed(
            title=ERROR_OCCURRED_TITLE,
            description="**This professor does not currently exist in the RateMyProf database!**",
            color=discord.Color.red()
        )
        await ctx.send(embed=error_embed)

        
async def main():
    async with client:
        await bot.start(token)

asyncio.run(main())
