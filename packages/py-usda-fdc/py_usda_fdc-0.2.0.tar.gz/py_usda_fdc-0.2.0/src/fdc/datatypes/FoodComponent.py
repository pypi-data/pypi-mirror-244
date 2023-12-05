from dataclasses import dataclass


@dataclass()
class FoodComponent:
    def __init__(self, id: int, name: str, data_points: int, gram_weight: int, is_refuse: bool, min_year_acquired: int,
                 percent_weight: float):
        self.id = id
        self.name = name
        self.data_points = data_points
        self.gram_weight = gram_weight
        self.is_refuse = is_refuse
        self.min_year_acquired = min_year_acquired
        self.percent_weight = percent_weight
