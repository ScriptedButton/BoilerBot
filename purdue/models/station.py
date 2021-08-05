from dataclasses import dataclass
from purdue.models import Item

@dataclass
class Station:
    name: str
    items: list[Item]