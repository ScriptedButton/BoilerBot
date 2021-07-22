#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# BoilerBot V1.1
# Written by Cole^2

from discord.ext import commands
import discord

import re

from classes import Parser, Course

description = "BoilerBot"

bot = commands.Bot(command_prefix='?', description=description)


def parseCourseInfo(subject, number):
    parser = Parser(subject, number)
    data = parser.getCourseInfo()
    title = data.find("h1", {"id": "course_preview_title"}).text
    description = data.find("hr").next_sibling
    description = re.sub("Credit Hours: .....", "", description)
    credits = data.find("strong").next_sibling
    course = Course(title, description, credits)
    return course


@bot.event
async def on_ready():
    print(f'Logged in as {bot.user} (ID: {bot.user.id})')
    print('------')


@bot.command()
async def courseinfo(ctx, subject, number):
    course = parseCourseInfo(subject, number)
    embed = discord.Embed(title=course.getTitle(),
                          description=course.getDescription(), color=0xdbce14)
    embed.add_field(name="Credit Hours",
                    value=course.getCredits(), inline=False)
    await ctx.send(embed=embed)

bot.run('. . .')
