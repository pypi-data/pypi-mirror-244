from dataclasses import dataclass

from .NutrientAcquisitionDetails import NutrientAcquisitionDetails


@dataclass()
class NutrientAnalysisDetails:
    def __init__(self, sub_sample_id: int, amount: float, nutrient_id: int, lab_method_description: str,
                 lab_method_original_description: str, lab_method_link: str, lab_method_technique: str,
                 nutrient_acquisition_details: dict, loq: float = None):
        self.sub_sample_id = sub_sample_id
        self.amount = amount
        self.nutrient_id = nutrient_id
        self.lab_method_description = lab_method_description
        self.lab_method_original_description = lab_method_original_description
        self.lab_method_link = lab_method_link
        self.lab_method_technique = lab_method_technique
        self.nutrient_acquisition_details = [NutrientAcquisitionDetails(**i) for i in nutrient_acquisition_details]

        # Were not added in the schema but are necessary
        self.loq = loq
