#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re

from classes import Parser, Course


def parseCourseInfo(subject, number):
    parser = Parser(subject, number)
    data = parser.getCourseInfo()

    title = data.find("h1", {"id": "course_preview_title"}).text

    description = data.find("hr").next_sibling
    description = re.sub("Credit Hours: .....", "", description)

    credits = data.find("strong").next_sibling

    course = Course(title, description, credits)

    return course
