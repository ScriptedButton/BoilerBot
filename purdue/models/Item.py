from dataclasses import dataclass


@dataclass
class Item:
    id: int
    name: str
    is_vegetarian: bool
    #allergens: list[Allergen]