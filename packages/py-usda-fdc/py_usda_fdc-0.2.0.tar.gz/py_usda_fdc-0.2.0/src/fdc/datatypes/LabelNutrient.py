from dataclasses import dataclass


@dataclass()
class LabelNutrient:
    def __init__(self, fat: dict = None, saturated_fat: dict = None, trans_fat: dict = None, cholesterol: dict = None,
                 sodium: dict = None, carbohydrates: dict = None, fiber: dict = None, sugars: dict = None,
                 protein: dict = None, calcium: dict = None, iron: dict = None, potassium: dict = None, calories: dict = None):

        self.fat = fat["value"]
        self.saturated_fat = saturated_fat["value"]
        self.trans_fat = trans_fat["value"]
        self.cholesterol = cholesterol["value"]
        self.sodium = sodium["value"]
        self.carbohydrates = carbohydrates["value"]
        self.fiber = fiber["value"]
        self.sugars = sugars["value"]
        self.protein = protein["value"]
        self.calcium = calcium["value"]
        self.iron = iron["value"]
        self.potassium = potassium["value"]
        self.calories = calories["value"]


