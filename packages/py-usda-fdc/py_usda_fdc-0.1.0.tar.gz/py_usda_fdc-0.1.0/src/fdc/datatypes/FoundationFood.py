from dataclasses import dataclass
from datetime import datetime
from .FoodCategory import FoodCategory
from .FoodComponent import FoodComponent
from .FoodNutrient import FoodNutrient
from .InputFoods import InputFoods
from .NutrientConversionFactor import NutrientConversionFactor
from .FoodAttribute import FoodAttribute
from .FoodPortion import FoodPortion
from .Food import Food


@dataclass()
class FoundationFood(Food):
    def __init__(self, fdc_id: int, data_type: str, description: str, food_class: str = None, foot_note: str = None,
                 is_historical_reference: bool = None, ndb_number: int = None, publication_date: str = None,
                 scientific_name: str = None, food_category: dict = None, food_components: dict = None,
                 food_nutrients: dict = None, food_portion: dict = None, input_foods: dict = None,
                 nutrient_conversion_factors: dict = None, food_attributes: list = None):
        super().__init__()
        self.fdc_id = fdc_id
        self.data_type = data_type
        self.description = description
        self.food_class = food_class
        self.foot_note = foot_note
        self.is_historical_reference = is_historical_reference
        self.ndb_number = ndb_number
        try:
            self.publication_date = datetime.strptime(publication_date,
                                                      "%m/%d/%Y").date() if publication_date else publication_date
        except ValueError:
            # If we are using list_foods, we get a different format for some reason
            self.publication_date = datetime.strptime(publication_date,
                                                      "%Y-%m-%d").date() if publication_date else publication_date
        self.scientific_name = scientific_name
        self.food_category = FoodCategory(**food_category) if food_category else None
        self.food_components = FoodComponent(**food_components) if food_components else None
        self.food_nutrients = [FoodNutrient(**food_nutrient) for food_nutrient in food_nutrients]
        self.food_portion = FoodPortion(**food_portion) if food_portion else food_portion
        self.input_foods = [InputFoods(**input_food) for input_food in input_foods] if input_foods else input_foods

        self.nutrient_conversion_factors = [NutrientConversionFactor(**nutrient_conversion_factor) for
                                            nutrient_conversion_factor in
                                            nutrient_conversion_factors] if nutrient_conversion_factors else nutrient_conversion_factors
        # Wasn't included in the schema but seems to be returned
        self.food_attributes = [FoodAttribute(**food_attribute) for food_attribute in
                                food_attributes] if food_attributes else food_attributes
