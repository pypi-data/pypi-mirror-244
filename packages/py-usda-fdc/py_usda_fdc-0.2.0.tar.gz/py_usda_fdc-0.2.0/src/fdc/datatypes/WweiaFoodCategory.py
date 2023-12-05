from dataclasses import dataclass


@dataclass()
class WweiaFoodCategory:
    def __init__(self, wweia_food_category_code: int = None, wweia_food_category_description: str = None):
        self.wweia_food_category_code= wweia_food_category_code
        self.wweia_food_category_description = wweia_food_category_description
