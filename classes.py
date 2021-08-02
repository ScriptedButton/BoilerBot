#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import urllib3

from dataclasses import dataclass
from datetime import datetime
from typing import List

import requests
from bs4 import BeautifulSoup, element

# disable 'InsecureRequestWarning: Unverified HTTPS request' warning
# TODO find a way to verify with purdue server.
urllib3.disable_warnings()


class Dining:
    def get_menus(self):
        req = requests.get("https://api.hfs.purdue.edu/menus/v2/locations")
        req = req.json()

        locations: List[Location] = []

        if req.get("Location", None) is not None:
            for location in req.get("Location"):
                locations.append(Location(location['Name']))

        return locations

    # this needs to be updated to work better, just wanted to get the basics down
    def get_menu(self, name):
        output = ""
        time = datetime.now()
        ftime = time.strftime("%m-%d-%Y")
        req = requests.get("https://api.hfs.purdue.edu/menus/v2/locations/{0}/{1}".format(name, ftime)).json()
        # print(req)
        for meal in req.get("Meals"):
            output += (meal.get("Name") + "\n")
        return output


@dataclass
class Location:
    name: str


@dataclass
class MenuItem:
    name: str


@dataclass
class Course:
    description: str
    credits: str
    title: str


# TO-DO: verify request somehow
class Parser:
    def __init__(self, subject: str, number: int) -> None:
        self.subject = subject
        self.number = number

    def get_course_url(self) -> str:
        req = requests.get(
            f"https://catalog.purdue.edu/search_advanced.php?cur_cat_oid=14&search_database=Search&search_db=Search&cpage=1&ecpage=1&ppage=1&spage=1&tpage=1&location=33&filter%5Bkeyword%5D={self.subject} {self.number}&filter%5Bexact_match%5D=1",
            verify=False
        )

        soup = BeautifulSoup(req.text, "lxml")
        course_url = "https://catalog.purdue.edu/" + \
                     soup.find_all("td", class_="td_dark")[1].find_all(
                         "a")[0]['href'].replace("_nopop", "")

        return course_url

    def get_course_info(self) -> element.Tag:
        course_url = self.get_course_url()
        req = requests.get(course_url, verify=False)

        soup = BeautifulSoup(req.text, "lxml")
        course_data = soup.find_all("td", class_="block_content_popup")[0]

        return course_data
