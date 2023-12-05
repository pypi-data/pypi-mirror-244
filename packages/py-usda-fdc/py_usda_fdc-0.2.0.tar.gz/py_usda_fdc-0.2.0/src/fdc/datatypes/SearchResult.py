from dataclasses import dataclass

from .FoodSearchCriteria import FoodSearchCriteria
from .SearchResultFood import SearchResultFood


@dataclass()
class SearchResult:
    def __init__(self, food_search_criteria: dict, total_hits: int = None, current_page: int = None,
                 total_pages: int = None, foods: list[dict] = None, page_list: list[int] = None,
                 aggregations: dict = None):
        self.food_search_criteria = FoodSearchCriteria(**food_search_criteria)
        self.total_hits = total_hits
        self.current_page = current_page
        self.total_pages = total_pages
        self.foods = [SearchResultFood(food) for food in foods] if foods else foods

        # Wasn't in schema but is needed
        self.page_list = page_list
        self.aggregations = aggregations
