import aiohttp

class Dining:
    def __init__(self):
        from purdue.models.location import Location
        self._LOCATION_URL = "https://api.hfs.purdue.edu/menus/v2/locations"
        self._locations: list[Location] = list()

    def get_location(self, name):
        for location in self.locations:
            if location.name == name:
                return location

    async def load(self):
        from purdue.models.address import Address
        async with aiohttp.ClientSession() as session:
            async with session.get(self._LOCATION_URL) as response:
                response_json = await response.json()
                for location in response_json.get("Location"):
                    location_obj = location.Location(
                        id=location.get("LocationId"),
                        name=location.get("Name"),
                        formal_name=location.get("FormalName"),
                        phone_number=location.get("PhoneNumber"),
                        latitude=location.get("Latitude"),
                        longitude=location.get("Longitude"),
                        short_name=location.get("ShortName"),
                        url=location.get("Url"),
                        google_place_id=location.get("GooglePlaceId"),
                        type=location.get("Type"),
                        transact_mobile_order_id=location.get("TransactMobileOrderId"),
                        address=address.Address(
                            street=location.get("Address").get("Street"),
                            city=location.get("Address").get("City"),
                            state=location.get("Address").get("State"),
                            zip_code=location.get("Address").get("ZipCode"),
                            country=location.get("Address").get("Country"),
                            country_code=location.get("Address").get("CountryCode")
                        ),
                        meals=None
                    )
                    self.locations.append(location_obj)


    @property
    def locations(self):
        return self._locations