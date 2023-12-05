from dataclasses import dataclass

from .Food import Food
from .FoodAttribute import FoodAttribute
from .FoodPortion import FoodPortion
from .InputFoodSurvey import InputFoodSurvey
from .WweiaFoodCategory import WweiaFoodCategory
from datetime import datetime


@dataclass()
class SurveyFood(Food):
    def __init__(self, fdc_id: int, data_type: str, description: str, start_date: str = None, end_date: str = None,
                 food_class: str = None, food_code: str = None,
                 publication_date: str = None, food_portion: dict = None, input_foods: dict = None,
                 wweia_food_category: dict = None, food_attributes: list = None):
        super().__init__()
        self.fdc_id = fdc_id
        self.data_type = data_type
        self.description = description
        self.start_date = datetime.strptime(start_date, "%m/%d/%Y").date() if start_date else start_date
        self.end_date = datetime.strptime(end_date, "%m/%d/%Y").date() if end_date else end_date
        self.food_class = food_class
        self.food_code = food_code
        try:
            self.publication_date = datetime.strptime(publication_date, "%m/%d/%Y").date()
        except ValueError:
            # If we are using list_foods, we get a different format for some reason
            self.publication_date = datetime.strptime(publication_date,
                                                      "%Y-%m-%d").date() if publication_date else publication_date
        self.food_portion = FoodPortion(**food_portion) if food_portion else food_portion
        self.input_foods = [InputFoodSurvey(**input_food) for input_food in input_foods] if input_foods else input_foods
        self.food_attributes = [FoodAttribute(**food_attribute) for food_attribute in
                                food_attributes] if food_attributes else food_attributes
        self.wweia_food_category = WweiaFoodCategory(
            **wweia_food_category) if wweia_food_category else wweia_food_category
