from dataclasses import dataclass


@dataclass()
class FoodSearchCriteria:
    def __init__(self, query: str, data_type: str = None, page_size: int = None, page_number: int = None,
                 sort_by: str = None, sort_order: str = None, brand_owner: str = None, trade_channel: list[str] = None,
                 start_date: str = None, end_date: str = None, general_search_input: str = None,
                 number_of_results_per_page: int = None, require_all_words: bool = None, food_types: list[str] = None):
        self.query = query
        self.data_type = data_type
        self.page_size = page_size
        self.page_number = page_number
        self.sort_by = sort_by
        self.sort_order = sort_order
        self.brand_owner = brand_owner
        self.trade_channel = trade_channel
        self.start_date = start_date
        self.end_date = end_date

        # Wasn't in schema but needed
        self.general_search_input = general_search_input
        self.number_of_results_per_page = number_of_results_per_page
        self.require_all_words = require_all_words
        self.food_types = food_types
