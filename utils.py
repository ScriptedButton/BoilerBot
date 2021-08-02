#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
from typing import List

from classes import Parser, Course, Dining, Location, Meal


def parse_course_info(subject: str, number: int) -> Course:
    parser = Parser(subject, number)
    data = parser.get_course_info()

    title = data.find("h1", {"id": "course_preview_title"}).text

    description = data.find("hr").next_sibling
    description = re.sub("Credit Hours: .....", "", description)

    course_credits = data.find("strong").next_sibling

    course = Course(description, course_credits, title)

    return course


def get_menus() -> List[Location]:
    return Dining().get_menus()


def get_menu(name) -> List[Meal]:
    return Dining().get_menu(name)
