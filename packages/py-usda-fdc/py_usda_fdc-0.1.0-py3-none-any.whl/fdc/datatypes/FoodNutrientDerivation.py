from dataclasses import dataclass

from .FoodNutrientSource import FoodNutrientSource


@dataclass()
class FoodNutritionDerivation:
    def __init__(self, id: int, code: str, description: str, food_nutrient_source: dict = None):
        self.id = id
        self.code = code
        self.description = description
        self.food_nutrient_source = FoodNutrientSource(
            **food_nutrient_source) if food_nutrient_source else food_nutrient_source
