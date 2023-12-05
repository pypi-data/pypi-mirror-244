from dataclasses import dataclass
from datetime import datetime
from .FoodNutrient import FoodNutrient


@dataclass()
class ExperimentalFood:
    def __init__(self, fdc_id: int = None, description:str = None, data_type:str = None, publication_date: str = None,
                 food_nutrients: list = None):
        self.fdc_id = fdc_id
        self.description = description
        self.data_type = data_type
        try:
            self.publication_date = datetime.strptime(publication_date,
                                                      "%m/%d/%Y").date() if publication_date else publication_date
        except ValueError:
            # If we are using list_foods, we get a different format for some reason
            self.publication_date = datetime.strptime(publication_date,
                                                      "%Y-%m-%d").date() if publication_date else publication_date
        self.food_nutrients = [FoodNutrient(**food_nutrient) for food_nutrient in food_nutrients] if food_nutrients else food_nutrients
