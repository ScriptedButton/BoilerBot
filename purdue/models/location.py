import datetime
from dataclasses import dataclass
import purdue.models.address as address
import purdue.models.meal as meal
import aiohttp
from typing import Optional


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
    address: address.Address
    meals: Optional[list[meal.Meal]]

    def get_meal_by_name(self, name):
        for meal in self.meals:
            if meal.name == name:
                return meal

    def get_station_by_name(self, meal, name):
        for station in meal.stations:
            if station.name == name:
                return station

    async def get_meals(self):
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
                                item.Item(
                                    id=item.get("Id"),
                                    name=item.get("Name"),
                                    is_vegetarian=item.get("IsVegetarian")
                                )
                            )
                        station_objects.append(
                            station.Station(
                                name=station.get("Name"),
                                items=item_objects

                            ))

                    self.meals = list()
                    self.meals.append(
                        meal.Meal(
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


