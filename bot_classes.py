import discord

PURDUE_COLOR_CODE = 0xCEB888

class MenuDropdown(discord.ui.Select):
    def __init__(self, menu_dropdown_view, user_id, dining):
        self.menu_options: list[discord.SelectOption] = list()
        self.menu_dropdown_view = menu_dropdown_view
        self.dining = dining
        self.state = "locations"
        self.current_location = None
        self.current_meal = None
        self.current_station = None
        self.user_id = user_id

        for item in self.dining.locations:
            self.menu_options.append(discord.SelectOption(label=item.name))

        super().__init__(placeholder='Select a location...', min_values=1, max_values=1, options=self.menu_options)

    async def display_meals(self, interaction):
        selected_location = self.values[0]
        location = self.dining.get_location(selected_location)
        await location.get_meals()

        meals_embed = discord.Embed(title=f"[Available Meals for {selected_location}]",
                                    description="\n".join([str(x.name) for x in location.meals]), color=PURDUE_COLOR_CODE)
        self.menu_options.clear()
        for meal in location.meals:
            self.menu_options.append(discord.SelectOption(label=meal.name))
        self.placeholder = "Select a meal..."
        await interaction.response.edit_message(embed=meals_embed, view=self.menu_dropdown_view)
        self.state = "meals"
        return location

    async def display_meal_stations(self, interaction, location, selected_meal):
        print(selected_meal)
        meal = location.get_meal_by_name(selected_meal)

        stations_embed = discord.Embed(title=f"[Available {meal.name} Stations at {self.current_location.name}]",
                                       description="\n".join([str(x.name) for x in meal.stations]),
                                       color=PURDUE_COLOR_CODE)
        self.menu_options.clear()
        for station in meal.stations:
            self.menu_options.append(discord.SelectOption(label=station.name))
        self.placeholder = "Select a station..."
        await interaction.response.edit_message(embed=stations_embed, view=self.menu_dropdown_view)
        self.state = "stations"
        self.current_meal = meal
        return meal.stations

    async def display_station_items(self, interaction, station):
        station = self.current_location.get_station_by_name(self.current_meal, station)
        items_embed = discord.Embed(title=f"[{station.name}]",
                                    description="\n".join([str(x.name) for x in station.items]),
                                    color=PURDUE_COLOR_CODE)
        await interaction.response.edit_message(embed=items_embed, view=self.menu_dropdown_view)
        for item in station.items:
            print(item.name)

    async def callback(self, interaction: discord.Interaction):
        if interaction.user.id == self.user_id:
            selected_item = self.values[0]
            if self.state == "locations":
                self.current_location = await self.display_meals(interaction)
            elif self.state == "meals":
                await self.display_meal_stations(interaction, self.current_location, selected_item)
            elif self.state == "stations":
                await self.display_station_items(interaction, selected_item)


class MenuDropdownView(discord.ui.View):
    def __init__(self, user_id, items):
        super().__init__()

        self.add_item(MenuDropdown(self, user_id, items))



