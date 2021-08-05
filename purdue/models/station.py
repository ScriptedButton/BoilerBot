from dataclasses import dataclass
import purdue.models.item as item

@dataclass
class Station:
    name: str
    items: list[item.Item]