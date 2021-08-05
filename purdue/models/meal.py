from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from purdue.models import Location, Station


@dataclass
class Meal:
    id: str
    name: str
    order: int
    status: str
    type: str
    location: 'Location'
    stations: list['Station']
    hours: dict[str, str]
