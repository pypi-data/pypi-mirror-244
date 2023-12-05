from dataclasses import dataclass

from .InputFood import InputFood


@dataclass()
class InputFoods:
    def __init__(self, id, food_description, input_food):
        self.id = id
        self.food_description = food_description
        self.input_food = InputFood(**input_food)
