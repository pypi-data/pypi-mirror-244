from dataclasses import dataclass

from .InputFood import InputFood
from .RetentionFactor import RetentionFactor


@dataclass()
class InputFoodSurvey:
    def __init__(self, id: int = None, amount: str = None, food_description: str = None, ingredient_code: int = None,
                 ingredient_description: str = None, ingredient_weight: float = None, portion_code: str = None,
                 portion_description: str = None, sequence_number: int = None, survey_flag: int = None,
                 unit: str = None, input_food: dict = None, retention_factor: dict = None):
        self.id = id
        self.amount = amount
        self.food_description = food_description
        self.ingredient_code = ingredient_code
        self.ingredient_description = ingredient_description
        self.ingredient_weight = ingredient_weight
        self.portion_code = portion_code
        self.portion_description = portion_description
        self.sequence_number = sequence_number
        self.survey_flag = survey_flag
        self.unit = unit
        self.input_food = InputFood(**input_food) if input_food else input_food
        self.retention_factor = RetentionFactor(**retention_factor) if retention_factor else retention_factor
