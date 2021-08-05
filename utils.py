from purdue.models.CourseParser import Parser
from purdue.models import Course
import re

def parse_course_info(subject: str, number: int) -> Course:
    parser = Parser(subject, number)
    data = parser.get_course_info()

    title = data.find("h1", {"id": "course_preview_title"}).text

    description = data.find("hr").next_sibling
    description = re.sub("Credit Hours: .....", "", description)

    course_credits = data.find("strong").next_sibling

    course = Course(description, course_credits, title)

    return course
