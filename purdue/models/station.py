from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from purdue.models import Item

@dataclass
class Station:
    name: str
    items: list['Item']