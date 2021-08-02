from classes import Dining

dining = Dining()
dining.get_menus()

menu = dining.get_menu("Wiley")
for meal in menu.Meals:
    print(f"==={meal.Name}===")
    print(f"Start Time: {meal.Hours.StartTime}")
    for station in meal.Stations:
        print(station.Name)
        for item in station.Items:
            print(f"- {item.Name}")