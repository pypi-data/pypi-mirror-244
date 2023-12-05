from dataclasses import dataclass

from .FoodAttributeType import FoodAttributeType


@dataclass()
class FoodAttribute:
    def __init__(self, id: int = None, sequence_number: int = None, value: str = None,
                 food_attribute_type: dict = None):
        self.id = id
        self.sequence_number = sequence_number
        self.value = value
        self.food_attribute_type = FoodAttributeType(
            **food_attribute_type) if food_attribute_type else food_attribute_type
