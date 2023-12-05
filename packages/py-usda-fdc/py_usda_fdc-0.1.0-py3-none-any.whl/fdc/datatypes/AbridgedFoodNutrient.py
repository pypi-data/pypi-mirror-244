from dataclasses import dataclass


@dataclass()
class AbridgedFoodNutrient:
    def __init__(self, number: int = None, name: str = None, amount: float = None, unit_name: str = None, derivation_code: str = None,
                 derivation_description: str = None):
        """
        Abridged Food Nutrient
        :param number: ID of Nutrient
        :param name: Name of Nutrient
        :param amount: Quantity of Nutrient
        :param unit_name: Unit of Nutrient
        :param derivation_code: Code that represents the derivation of how the amount was calculated. exmaple: LCCD
        :param derivation_description: Description of Derivation Code. Example: Calculated from a daily value percentage
        per serving size measure
        """
        self.number = number
        self.name = name
        self.amount = amount
        self.unit_name = unit_name
        self.derivation_code = derivation_code
        self.derivation_description = derivation_description
