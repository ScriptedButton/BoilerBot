import requests
from bs4 import BeautifulSoup, element

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