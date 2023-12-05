from dataclasses import dataclass


@dataclass()
class FoodGroup:
    def __init__(self, id, code, description):
        self.id = id
        self.code = code
        self.description = description