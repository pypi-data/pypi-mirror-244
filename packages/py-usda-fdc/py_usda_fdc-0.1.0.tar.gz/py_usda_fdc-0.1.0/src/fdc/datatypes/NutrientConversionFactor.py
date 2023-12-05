from dataclasses import dataclass


@dataclass()
class NutrientConversionFactor:
    def __init__(self, id, protein_value=0, fat_value=0, carbohydrate_value=0, value=0, type=None, name=None):
        self.id = id
        self.protein_value = protein_value
        self.fat_value = fat_value
        self.carbohydrate_value = carbohydrate_value
        self.value = value
        self.type = type
        self.name = name
