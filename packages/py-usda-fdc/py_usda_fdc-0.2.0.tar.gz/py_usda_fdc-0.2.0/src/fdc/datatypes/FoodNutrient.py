from dataclasses import dataclass

from .Nutrient import Nutrient
from .FoodNutrientDerivation import FoodNutritionDerivation
from .NutrientAnalysisDetails import NutrientAnalysisDetails


@dataclass()
class FoodNutrient:
    def __init__(self, id: int = None, amount: float = None, data_points: int = None, min: float = None,
                 max: float = None, median: float = None, type: str = None, nutrient: dict = None,
                 food_nutrient_derivation: dict = None, nutrient_analysis_details: dict = None,
                 min_year_acquired: int = None, loq: float = None):
        self.id = id
        self.amount = amount
        self.data_points = data_points
        self.min = min
        self.max = max
        self.median = median
        self.type = type
        self.Nutrient = Nutrient(**nutrient) if nutrient else nutrient
        self.food_nutrient_derivation = FoodNutritionDerivation(
            **food_nutrient_derivation) if food_nutrient_derivation else None
        self.nutrient_analysis_details = [NutrientAnalysisDetails(**i) for i in
                                          nutrient_analysis_details] if nutrient_analysis_details else None

        # Were not included in the schema, but necessary
        self.min_year_acquired = min_year_acquired
        self.loq = loq
