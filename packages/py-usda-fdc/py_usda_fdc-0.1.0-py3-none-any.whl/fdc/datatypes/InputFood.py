from dataclasses import dataclass

from .FoodGroup import FoodGroup
from .FoodAttributeType import FoodAttributeType


@dataclass()
class InputFood:
    def __init__(self, fdc_id, description, publication_date, food_attribute_types, food_class, total_refuse, data_type,
                 food_group):
        self.fdc_id = fdc_id
        self.description = description
        self.publication_date = publication_date
        self.food_attribute_types = [FoodAttributeType(**food_attribute_type) for food_attribute_type in
                                     food_attribute_types] if food_attribute_types else food_attribute_types
        self.food_class = food_class
        self.total_refuse = total_refuse
        self.data_type = data_type
        self.food_group = FoodGroup(**food_group)
