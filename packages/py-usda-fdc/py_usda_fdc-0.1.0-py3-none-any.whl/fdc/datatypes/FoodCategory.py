from dataclasses import dataclass


@dataclass()
class FoodCategory:
    def __init__(self, id, code, description):
        self.id = id
        self.code = code
        self.description = description
