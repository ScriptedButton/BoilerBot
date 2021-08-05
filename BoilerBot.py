#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# BoilerBot V1.1
# Written by Cole^2

import asyncio
import os
from concurrent.futures import ThreadPoolExecutor

import discord
from discord.ext import commands

from purdue.models.Dining import Dining

from bbclasses import MenuDropdownView
from utils import parse_course_info
import ratemyprofessor

description = "BoilerBot"
bot = commands.Bot(command_prefix='?', description=description, status="Boiler Up! Hammer Down!", help_command=None)

token = os.getenv("BOT_TOKEN")

PURDUE_COLOR_CODE = 0xCEB888

loop = asyncio.get_event_loop()

if token is None:
    print("Unable to retrieve data for env variable `BOT_TOKEN`. Exitting!")
    exit(0)



@bot.event
async def on_ready():
    print(f'Logged in as {bot.user} (ID: {bot.user.id})')
    print('------')
    bot_status = discord.Streaming(name="Boiler Up! Hammer Down!", url="https://purdue.edu")
    await bot.change_presence(activity=bot_status)

@bot.command()
async def help(ctx):
    desc = "[1] ?course_info [subject] [number] - Gives you course information." \
           "\n[2] ?menus - Pulls dining menus from Purdue." \
           "\n[3] ?rateprof [name] - Gives details about a specific professor."
    help_embed = discord.Embed(title="[BoilerBot Documentation]",
                               description=desc,
                               color=PURDUE_COLOR_CODE)
    help_embed.set_footer(text="Written by Cole^2 | BoilerBot 2021")
    await ctx.send(embed=help_embed)


@bot.command()
async def menus(ctx):
    try:
        dining = Dining()
        await dining.load()
        locations = dining.locations
        locations_embed = discord.Embed(title="[All Locations]",
                              description="\n".join([str(x.name) for x in locations]), color=PURDUE_COLOR_CODE)
        menu_dropdown_view_obj = MenuDropdownView(ctx.message.author.id, dining)
        await ctx.send(embed=locations_embed, view=menu_dropdown_view_obj)
    except Exception as e:
        error_embed = discord.Embed(title="An Error Occured", description=f"{str(e)}\n\nThis usually means Purdue has no data on an item!", color=discord.Color.red())
        await ctx.send(embed=error_embed)


@bot.command(name="courseinfo")
async def course_info(ctx, subject: str, number: int):
    try:
        course = await loop.run_in_executor(
            ThreadPoolExecutor(), parse_course_info, subject, number
        )
        embed = discord.Embed(title=course.title,
                              description=course.description, color=PURDUE_COLOR_CODE)
        embed.add_field(name="Credit Hours",
                        value=course.credits, inline=False)
        await ctx.send(embed=embed)
    except Exception as e:
        error_embed = discord.Embed(title="An Error Occured",
                                    description=f"**{str(e)}\n\nThis usually means Purdue has no data on an item!**",
                                    color=discord.Color.red())
        await ctx.send(embed=error_embed)

@bot.command(name="rateprof")
async def rate_prof(ctx, *, name):
    try:
        if name.lower() == "mitch daniels":
            prof_embed = discord.Embed(title="[Mitch Daniels]", description="Literally a god among men", color=PURDUE_COLOR_CODE)
            await ctx.send(embed=prof_embed)
        else:
            purdue = await loop.run_in_executor(ThreadPoolExecutor(), ratemyprofessor.get_school_by_name, "Purdue")
            print(str(purdue))
            prof = await loop.run_in_executor(ThreadPoolExecutor(), ratemyprofessor.get_professor_by_school_and_name, purdue, name)
            print(str(prof))
            would_take_again = None
            if prof.would_take_again is int:
                would_take_again = f"{round(prof.would_take_again)}%"
            else:
                would_take_again = "N/A"

            desc = f"Professor Difficulty: **{prof.difficulty or None}**" \
                   f"\nProfessor Rating: **{prof.rating or None}**" \
                   f"\nNumber of Ratings: **{prof.num_ratings or None}**" \
                   f"\nDepartment: **{prof.department or None}**" \
                   f"\nWould Take Again: **{would_take_again or None}**"
            prof_embed = discord.Embed(title=f"[{prof.name or None}]", description=desc, color=PURDUE_COLOR_CODE)
            await ctx.send(embed=prof_embed)
    except Exception:
        error_embed = discord.Embed(title="An Error Occured",
                                    description=f"**This professor does not currently exist in the RateMyProf database!**",
                                    color=discord.Color.red())
        await ctx.send(embed=error_embed)

bot.run(token)