from dataclasses import dataclass
from datetime import datetime
from .FoodCategory import FoodCategory


@dataclass()
class MarketAcquisitionFood:
    def __init__(self, fdc_id: int, data_type: str, description: str, food_class: str = None, store_city: str = None,
                 label_weight: str = None, location: str = None, acquisition_date: str = None,
                 brand_description: str = None, sample_lot_number: str = None, food_components: list = None,
                 store_name: str = None, store_state: str = None, upc_code: str = None,
                 food_category: dict = None, publication_date: str = None):
        self.fdc_id = fdc_id
        self.description = description
        self.data_type = data_type
        self.food_class = food_class
        self.food_components = food_components
        self.label_weight = label_weight
        self.location = location
        self.acquisition_date = datetime.strptime(acquisition_date, "%m/%d/%Y").date()
        self.brand_description = brand_description
        self.sample_lot_number = sample_lot_number
        self.store_city = store_city
        self.store_name = store_name
        self.store_state = store_state
        self.upc_code = upc_code
        self.food_category = FoodCategory(**food_category) if food_category else None
        self.publication_date = datetime.strptime(publication_date, "%m/%d/%Y").date()
