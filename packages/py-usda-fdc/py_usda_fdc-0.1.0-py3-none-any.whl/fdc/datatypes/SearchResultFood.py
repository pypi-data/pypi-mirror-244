from dataclasses import dataclass

from .Food import Food
from .FoodNutrient import FoodNutrient
from datetime import datetime


@dataclass()
class SearchResultFood(Food):
    def __init__(self, fdc_id: int = None, data_type: str = None, description: str = None, publication_date: str = None,
                 food_nutrients: dict = None, ndb_number: int = None, brand_owner: str = None, gtin_upc: str = None,
                 food_code: str = None, scientific_name: str = None, ingredients: str = None,
                 additional_descriptions: str = None, all_highlight_fields: str = None, score: float = None):
        super().__init__()
        self.fdc_id = fdc_id
        self.data_type = data_type
        self.description = description
        self.publication_date = datetime.strptime(publication_date,
                                                  "%m/%d/%Y").date() if publication_date else publication_date
        self.food_nutrients = [FoodNutrient(**food_nutrient) for food_nutrient in
                               food_nutrients] if food_nutrients else food_nutrients
        self.food_code = food_code
        self.scientific_name = scientific_name
        self.brand_owner = brand_owner
        self.gtin_upc = gtin_upc
        self.ingredients = ingredients
        self.ndb_number = ndb_number
        self.additional_descriptions = additional_descriptions
        self.all_highlight_fields = all_highlight_fields
        self.score = score
