#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from dataclasses import dataclass

from bs4 import BeautifulSoup
import requests


@dataclass
class Course:
    description: str
    credits: str
    title: str


class Parser:
    def __init__(self, subject, number):
        self.subject = subject
        self.number = number

    def getCourseUrl(self):
        req = requests.get("https://catalog.purdue.edu/search_advanced.php?cur_cat_oid=14&search_database=Search&search_db=Search&cpage=1&ecpage=1&ppage=1&spage=1&tpage=1&location=33&filter%5Bkeyword%5D={0} {1}&filter%5Bexact_match%5D=1".format(
            self.subject, self.number), verify=False)
        soup = BeautifulSoup(req.text, "lxml")
        courseUrl = "https://catalog.purdue.edu/" + \
            soup.find_all("td", class_="td_dark")[1].find_all(
                "a")[0]['href'].replace("_nopop", "")
        return courseUrl

    def getCourseInfo(self):
        courseUrl = self.getCourseUrl()
        req = requests.get(courseUrl, verify=False)
        soup = BeautifulSoup(req.text, "lxml")
        courseData = soup.find_all("td", class_="block_content_popup")[0]
        return courseData
