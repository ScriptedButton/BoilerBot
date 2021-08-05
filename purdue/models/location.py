import datetime
from dataclasses import dataclass
import aiohttp
from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from purdue.models import Address, Meal


@dataclass
class Location:
    id: str
    name: str
    formal_name: str
    phone_number: str
    latitude: str
    longitude: str
    short_name: str
    url: str
    google_place_id: str
    type: str
    transact_mobile_order_id: str
    address: 'Address'
    meals: Optional[list['Meal']]

    def get_meal_by_name(self, name):
        for meal in self.meals:
            if meal.name == name:
                return meal

    def get_station_by_name(self, meal, name):
        for station in meal.stations:
            if station.name == name:
                return station

    async def get_meals(self):
        from purdue.models import Item, Station, Meal
        async with aiohttp.ClientSession() as session:
            async with session.get(
                    f"https://api.hfs.purdue.edu/menus/v2/locations/{self.name}/{datetime.date.today()}"
            ) as response:
                response_json = await response.json()
                for meal in response_json.get("Meals"):
                    station_objects: list[station.Station] = list()
                    for station in meal.get("Stations"):
                        item_objects: list[item.Item] = list()
                        for item in station.get("Items"):
                            item_objects.append(
                                Item(
                                    id=item.get("Id"),
                                    name=item.get("Name"),
                                    is_vegetarian=item.get("IsVegetarian")
                                )
                            )
                        station_objects.append(
                            Station(
                                name=station.get("Name"),
                                items=item_objects

                            ))

                    self.meals = list()
                    self.meals.append(
                        Meal(
                            id=meal.get("Id"),
                            name=meal.get("Name"),
                            order=meal.get("Order"),
                            status=meal.get("Status"),
                            type=meal.get("Type"),
                            location=self,
                            stations=station_objects,
                            hours={"StartTime": "dsa", "EndTime": "str"}
                        )
                    )


