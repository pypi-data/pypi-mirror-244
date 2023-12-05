from dataclasses import dataclass
from datetime import datetime
from .FoodNutrient import FoodNutrient
from .FoodUpdateLog import FoodUpdateLog
from .LabelNutrient import LabelNutrient
from .Food import Food


@dataclass()
class BrandedFood(Food):
    def __init__(self, fdc_id: int, data_type: str, description: str, food_class: str = None,
                 publication_date: str = None, food_nutrients: dict = None, available_date: str = None,
                 brand_owner: str = None, data_source: str = None, gtin_upc: str = None,
                 household_serving_full_text: str = None, ingredients: str = None, modified_date: str = None,
                 serving_size: float = None, serving_size_unit: str = None, preparation_state_code: str = None,
                 branded_food_category: str = None, trade_channel: list[str] = None, gpc_class_code: int = None,
                 food_update_log: dict = None, label_nutrient: dict = None):
        super().__init__()
        self.fdc_id = fdc_id
        self.available_date = datetime.strptime(available_date,
                                                "%m/%d/%Y").date() if available_date else available_date
        self.brand_owner = brand_owner
        self.data_source = data_source
        self.data_type = data_type
        self.description = description
        self.food_class = food_class
        self.gtin_upc = gtin_upc
        self.household_serving_full_text = household_serving_full_text
        self.ingredients = ingredients
        self.modified_date = datetime.strptime(modified_date,
                                               "%m/%d/%Y").date() if modified_date else modified_date
        self.publication_date = datetime.strptime(publication_date,
                                                  "%m/%d/%Y").date() if publication_date else publication_date
        self.serving_size = serving_size
        self.serving_size_unit = serving_size_unit
        self.preparation_state_code = preparation_state_code
        self.branded_food_category = branded_food_category
        self.trade_channel = trade_channel
        self.gpc_class_code = gpc_class_code
        self.food_nutrients = [FoodNutrient(**food_nutrient) for food_nutrient in
                               food_nutrients] if food_nutrients else food_nutrients
        self.food_update_log = FoodUpdateLog(**food_update_log) if food_update_log else food_update_log
        self.label_nutrients = LabelNutrient(**label_nutrient) if label_nutrient else label_nutrient
