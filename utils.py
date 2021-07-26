#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from typing import List
import re

from classes import Parser, Course, Dining, Location


def parseCourseInfo(subject: str, number: int) -> Course:
    parser = Parser(subject, number)
    data = parser.getCourseInfo()

    title = data.find("h1", {"id": "course_preview_title"}).text

    description = data.find("hr").next_sibling
    description = re.sub("Credit Hours: .....", "", description)

    credits = data.find("strong").next_sibling

    course = Course(description, credits, title)

    return course


def getMenus() -> List[Location]:
    return Dining().getMenus()
