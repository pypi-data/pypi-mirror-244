from dataclasses import dataclass


@dataclass()
class FoodNutrientSource:
    def __init__(self, id: int, code: str, description: str):
        self.id = id
        self.code = code
        self.description = description
