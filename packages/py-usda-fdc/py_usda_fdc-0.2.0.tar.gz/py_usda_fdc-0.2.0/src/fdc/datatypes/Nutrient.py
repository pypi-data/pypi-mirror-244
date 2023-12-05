from dataclasses import dataclass


@dataclass()
class Nutrient:
    def __init__(self, id: int, number: str, name: str, rank: int, unit_name: str):
        self.id = id
        self.number = number
        self.name = name
        self.rank = rank
        self.unit_name = unit_name