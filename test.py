from purdue.models import Dining
import asyncio

loop = asyncio.get_event_loop()


async def main():
    dining = Dining()
    await dining.load()
    for location in dining.locations:
        #print(location)
        await location.get_meals()
        print(f"[{location.name}]")
        if location.meals:
            for meal in location.meals:
                print(f"[{meal.name}]")
                for station in meal.stations:
                    print(f"==={station.name}===")
                    for item in station.items:
                        print(f"- {item.name}")

loop.run_until_complete(main())
