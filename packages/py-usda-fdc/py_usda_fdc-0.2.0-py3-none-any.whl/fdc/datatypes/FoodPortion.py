from dataclasses import dataclass

from .MeasureUnit import MeasureUnit


@dataclass()
class FoodPortion:
    def __init__(self, id: int = None, amount: float = None, data_points: int = None, gram_weight: float = None,
                 min_year_acquired: int = None, modifier: str = None, portion_description: str = None,
                 sequence_number: int = None, measure_unit: dict = None):
        self.id = id
        self.amount = amount
        self.data_points = data_points
        self.gram_weight = gram_weight
        self.min_year_acquired = min_year_acquired
        self.modifier = modifier
        self.portion_description = portion_description
        self.sequence_number = sequence_number
        self.measure_unit = MeasureUnit(**measure_unit) if measure_unit else measure_unit
