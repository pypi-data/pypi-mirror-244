from dataclasses import dataclass


@dataclass()
class FoodAttributeType:
    def __init__(self, id: int = None, name: str = None, description: str = None):
        self.id = id
        self.name = name
        self.description = description