from dataclasses import dataclass
from datetime import datetime


@dataclass()
class NutrientAcquisitionDetails:
    def __init__(self, sample_unit_id: int, purchase_date: str, store_city: str, store_state: str,
                 packer_city: str = None, packer_state: str = None):
        self.sample_unit_id = sample_unit_id
        self.purchase_date = datetime.strptime(purchase_date, "%m/%d/%Y").date()
        self.store_city = store_city
        self.store_state = store_state

        # Had to add it even though it wasn't in the schema
        self.packer_city = packer_city
        self.packer_state = packer_state
