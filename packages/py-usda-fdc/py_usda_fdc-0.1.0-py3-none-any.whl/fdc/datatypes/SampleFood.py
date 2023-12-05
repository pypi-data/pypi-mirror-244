from dataclasses import dataclass
from datetime import datetime
from .FoodComponent import FoodComponent
from .FoodNutrient import FoodNutrient
from .FoodCategory import FoodCategory
from .FoodAttribute import FoodAttribute
from .FoodPortion import FoodPortion
from .Food import Food


@dataclass()
class SampleFood(Food):
    def __init__(self, fdc_id: int, data_type: str, description: str, food_class: str = None,
                 food_attributes: list = None, food_nutrients: str = None, food_portions: list = None,
                 food_components: list = None, food_category: dict = None, publication_date: str = None):
        super().__init__()
        self.fdc_id = fdc_id
        self.description = description
        self.publication_date = datetime.strptime(publication_date, "%m/%d/%Y").date() if publication_date else publication_date
        self.data_type = data_type
        self.food_class = food_class
        self.food_components = [FoodComponent(**i) for i in food_components] if food_components else food_components
        self.food_attributes = [FoodAttribute(**food_attribute) for food_attribute in food_attributes] if food_attributes else food_attributes
        self.food_nutrients = [FoodNutrient(**i) for i in food_nutrients] if food_nutrients else food_nutrients
        self.food_portions = [FoodPortion(**food_portion) for food_portion in food_portions] if food_portions else food_portions
        self.food_category = FoodCategory(**food_category) if food_category else food_category
