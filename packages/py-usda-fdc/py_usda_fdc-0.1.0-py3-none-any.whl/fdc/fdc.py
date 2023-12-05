import json
from .datatypes import AbridgedFood, FoundationFood, MarketAcquisitionFood, SampleFood, BrandedFood,\
    SRLegacyFood, SurveyFood, Food, ExperimentalFood, SearchResult
import requests
import humps
from typing import List


class FDC:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://api.nal.usda.gov/fdc/v1/"

    def get_food(self, id_: str, format_: str = "full", nutrients: List[int] = None) -> Food:
        """
        Retrieves a single food item by an FDC ID. Optional format and nutrients can be specified.

        :param id\_: FDC id of the food to retrieve
        :param format\_: Optional. 'abridged' for an abridged set of elements, 'full' for all elements (default).
        :param nutrients: Optional. List of up to 25 nutrient numbers. Only the nutrient information for the specified nutrients will be returned. Should be comma separated list (e.g. nutrients=203, 204) or repeating parameters (e.g. nutrients=203&nutrients=204). If a food does not have any matching nutrients, the food will be returned with an empty foodNutrients element.
        :return: `Food` object
        """
        req = self._call_food(id_, format_, nutrients)
        item = humps.decamelize(json.loads(req.text))
        food = self._match_data_type(item, format_)
        return food

    def get_food_raw(self, id_: str, format_: str = "full", nutrients: List[int] = None) -> str:
        """
        Retrieves a single food item by an FDC ID. Optional format and nutrients can be specified.

        :param id\_: FDC id of the food to retrieve
        :param format\_: Optional. 'abridged' for an abridged set of elements, 'full' for all elements (default).
        :param nutrients: Optional. List of up to 25 nutrient numbers. Only the nutrient information for the specified nutrients will be returned. Should be comma separated list (e.g. nutrients=203, 204) or repeating parameters (e.g. nutrients=203&nutrients=204). If a food does not have any matching nutrients, the food will be returned with an empty foodNutrients element.
        :return: `str` of json
        """
        req = self._call_food(id_, format_, nutrients)
        return req.text

    def _call_food(self, id_: str, format_: str = "full", nutrients: List[int] = None) -> requests.Response:
        url = self.base_url + f"food/{str(id_)}"
        payload = {"api_key": self.api_key, "format": format_}
        if nutrients:
            payload["nutrients"] = nutrients
        req = requests.get(url, payload)
        if req.status_code != 200:
            req.raise_for_status()
        return req

    def get_foods(self, ids: List[str], format_: str = "full", nutrients: List[int] = None) -> List[Food]:
        """
        Retrieves a list of food items by a list of up to 20 FDC IDs. Optional format and nutrients can be specified. Invalid FDC ID's or ones that are not found are omitted and an empty set is returned if there are no matches.

        :param ids: List of multiple FDC ID's
        :param format\_: Optional. 'abridged' for an abridged set of elements, 'full' for all elements (default).
        :param nutrients: Optional. List of up to 25 nutrient numbers. Only the nutrient information for the specified nutrients will be returned. Should be comma separated list (e.g. nutrients=203, 204) or repeating parameters (e.g. nutrients=203&nutrients=204). If a food does not have any matching nutrients, the food will be returned with an empty foodNutrients element.
        :return: List of `Food` Objects
        """
        req = self._call_foods(ids, format_, nutrients)
        result_json = humps.decamelize(json.loads(req.text))
        foods = []
        for item in result_json:
            food = self._match_data_type(item, format_)
            foods.append(food)
        return foods

    def get_foods_raw(self, ids: List[str], format_: str = "full", nutrients: List[int] = None) -> str:
        """
        Retrieves a list of food items by a list of up to 20 FDC IDs. Optional format and nutrients can be specified. Invalid FDC ID's or ones that are not found are omitted and an empty set is returned if there are no matches.

        :param ids: List of multiple FDC ID's
        :param format\_: Optional. 'abridged' for an abridged set of elements, 'full' for all elements (default).
        :param nutrients: Optional. List of up to 25 nutrient numbers. Only the nutrient information for the specified nutrients will be returned. Should be comma separated list (e.g. nutrients=203, 204) or repeating parameters (e.g. nutrients=203&nutrients=204). If a food does not have any matching nutrients, the food will be returned with an empty foodNutrients element.
        :return: List of `str` jsons
        """
        req = self._call_foods(ids, format_, nutrients)
        return req.text

    def _call_foods(self, ids: List[str], format_: str = "full", nutrients: List[int] = None) -> requests.Response:
        url = self.base_url + f"foods"
        payload = {"api_key": self.api_key, "format": format_, "fdcIds": ids}
        if nutrients:
            payload["nutrients"] = nutrients
        req = requests.get(url, payload)
        if req.status_code != 200:
            req.raise_for_status()
        return req

    def get_foods_list(self, data_type: str = None, page_size: int = None, page_number: int = None, sort_by: str = None,
                       sort_order: str = None) -> list[AbridgedFood]:
        """
        Retrieves a paged list of foods. Use the pageNumber parameter to page through the entire result set.

        :param data_type: Optional. Filter on a specific data type; specify one or more values in an array.
        :param page_size: Optional. Maximum number of results to return for the current page. Default is 50. Min=1, Max=200
        :param page_number: Optional. Page number to retrieve. The offset into the overall result set is expressed as (pageNumber * pageSize)
        :param sort_by: Optional. Specify one of the possible values to sort by that field. Note, dataType.keyword will be dataType and lowercaseDescription.keyword will be description in future releases. Can be any of the following `["dataType.keyword", "lowercaseDescription.keyword", "fdcId", "publishedDate"]`
        :param sort_order: Optional. The sort direction for the results. Only applicable if sortBy is specified. Can be any of the following `["asc", "desc"]`
        :return: List of `AbridgedFood` objects
        """
        req = self._call_foods_list(data_type, page_size, page_number, sort_by, sort_order)
        result_json = humps.decamelize(json.loads(req.text))
        foods = []
        for item in result_json:
            food = AbridgedFood(**item)
            foods.append(food)
        return foods

    def get_foods_list_raw(self, data_type: str = None, page_size: int = None, page_number: int = None,
                           sort_by: str = None, sort_order: str = None) -> str:
        """
        Retrieves a paged list of foods. Use the pageNumber parameter to page through the entire result set.

        :param data_type: Optional. Filter on a specific data type; specify one or more values in an array.
        :param page_size: Optional. Maximum number of results to return for the current page. Default is 50. Min=1, Max=200
        :param page_number: Optional. Page number to retrieve. The offset into the overall result set is expressed as (pageNumber * pageSize)
        :param sort_by: Optional. Specify one of the possible values to sort by that field. Note, dataType.keyword will be dataType and lowercaseDescription.keyword will be description in future releases. Can be any of the following `["dataType.keyword", "lowercaseDescription.keyword", "fdcId", "publishedDate"]`
        :param sort_order: Optional. The sort direction for the results. Only applicable if sortBy is specified. Can be any of the following `["asc", "desc"]`
        :return: List of `str` jsons
        """
        req = self._call_foods_list(data_type, page_size, page_number, sort_by, sort_order)
        return req.text

    def _call_foods_list(self, data_type: str = None, page_size: int = None, page_number: int = None,
                         sort_by: str = None, sort_order: str = None) -> requests.Response:
        url = self.base_url + f"foods/list"
        payload = {"api_key": self.api_key}
        if data_type:
            payload["dataType"] = data_type
        if page_size:
            payload["pageSize"] = page_size
        if page_number:
            payload["pageNumber"] = page_number
        if sort_by:
            payload["sortBy"] = sort_by
        if sort_order:
            payload["sortOrder"] = sort_order
        req = requests.get(url, payload)
        if req.status_code != 200:
            req.raise_for_status()
        return req

    def get_foods_search(self, query: str, data_type: str = None, page_size: int = None, page_number: int = None,
                         sort_by: str = None, sort_order: str = None, brand_owner: str = None) -> SearchResult:
        """
        Search for foods using keywords. Results can be filtered by dataType and there are options for result page sizes or sorting.

        :param query: One or more search terms. The string may include search operators: https://fdc.nal.usda.gov/help.html#bkmk-2
        :param data_type: Optional. Filter on a specific data type; specify one or more values in an array. Available values : Branded, Foundation, Survey (FNDDS), SR Legacy
        :param page_size: Optional. Maximum number of results to return for the current page. Default is 50. Min is 1, Max is 200
        :param page_number: Optional. Page number to retrieve. The offset into the overall result set is expressed as (pageNumber * pageSize)
        :param sort_by: Optional. Specify one of the possible values to sort by that field. Note, dataType.keyword will be dataType and lowercaseDescription.keyword will be description in future releases. Available values : dataType.keyword, lowercaseDescription.keyword, fdcId, publishedDate
        :param sort_order: Optional. The sort direction for the results. Only applicable if sortBy is specified. Available values : asc, desc
        :param brand_owner: Optional. Filter results based on the brand owner of the food. Only applies to Branded Foods
        :return: `str` or `SearchResult` object
        """
        req = self._call_foods_search(query, data_type, page_size, page_number, sort_by, sort_order, brand_owner)
        result_json = humps.decamelize(json.loads(req.text))
        search_result = SearchResult(**result_json)
        return search_result

    def get_foods_search_raw(self, query: str, data_type: str = None, page_size: int = None, page_number: int = None,
                             sort_by: str = None, sort_order: str = None, brand_owner: str = None) -> str:
        """
        Search for foods using keywords. Results can be filtered by dataType and there are options for result page sizes or sorting.

        :param query: One or more search terms. The string may include search operators: https://fdc.nal.usda.gov/help.html#bkmk-2
        :param data_type: Optional. Filter on a specific data type; specify one or more values in an array. Available values : Branded, Foundation, Survey (FNDDS), SR Legacy
        :param page_size: Optional. Maximum number of results to return for the current page. Default is 50. Min is 1, Max is 200
        :param page_number: Optional. Page number to retrieve. The offset into the overall result set is expressed as (pageNumber * pageSize)
        :param sort_by: Optional. Specify one of the possible values to sort by that field. Note, dataType.keyword will be dataType and lowercaseDescription.keyword will be description in future releases. Available values : dataType.keyword, lowercaseDescription.keyword, fdcId, publishedDate
        :param sort_order: Optional. The sort direction for the results. Only applicable if sortBy is specified. Available values : asc, desc
        :param brand_owner: Optional. Filter results based on the brand owner of the food. Only applies to Branded Foods
        :return: `str` of json
        """
        req = self._call_foods_search(query, data_type, page_size, page_number, sort_by, sort_order, brand_owner)
        return req.text

    def _call_foods_search(self, query: str, data_type: str = None, page_size: int = None, page_number: int = None,
                           sort_by: str = None, sort_order: str = None, brand_owner: str = None) -> requests.Response:
        url = self.base_url + f"foods/search"
        payload = {"api_key": self.api_key, "query": query}
        if data_type:
            payload["dataType"] = data_type
        if page_size:
            payload["pageSize"] = page_size
        if page_number:
            payload["pageNumber"] = page_number
        if sort_by:
            payload["sortBy"] = sort_by
        if sort_order:
            payload["sortOrder"] = sort_order
        if brand_owner:
            payload["brandOwner"] = brand_owner
        req = requests.get(url, payload)
        if req.status_code != 200:
            req.raise_for_status()
        return req

    def get_json_specs(self) -> str:
        """
        The OpenAPI 3.0 specification for the FDC API rendered as JSON (JavaScript Object Notation)

        :return: Returns the documentation found at https://app.swaggerhub.com/apis/fdcnal/food-data_central_api/1.0.1 in JSON notation
        """
        url = self.base_url + f"json-spec?api_key={self.api_key}"
        req = requests.get(url)
        if req.status_code != 200:
            req.raise_for_status()
        return req.text

    def get_yaml_specs(self) -> str:
        """
        The OpenAPI 3.0 specification for the FDC API rendered as YAML (YAML Ain't Markup Language)

        :return: Returns the documentation found at https://app.swaggerhub.com/apis/fdcnal/food-data_central_api/1.0.1 in YAML notation
        """
        url = self.base_url + f"yaml-spec?api_key={self.api_key}"
        req = requests.get(url)
        if req.status_code != 200:
            req.raise_for_status()
        return req.text

    def _match_data_type(self, item: dict, _format: str) -> Food:
        """
        Used to serialize the FoodItem properly.

        :param item: JSON of the food item.
        :param _format: Was the query Full or Abridged
        :return: A `Food` class
        """
        food = None
        if _format == "abridged":
            food = AbridgedFood(**item)
        elif item["data_type"] == "Branded":
            food = BrandedFood(**item)
        elif item["data_type"] == "Foundation":
            food = FoundationFood(**item)
        elif item["data_type"] == "SR Legacy":
            food = SRLegacyFood(**item)
        elif item["data_type"] == "Survey (FNDDS)":
            food = SurveyFood(**item)
        elif item["data_type"] == "Market Acquisition":
            food = MarketAcquisitionFood(**item)
        elif item["data_type"] == "Sample":
            food = SampleFood(**item)
        elif item["data_type"] == "Experimental":
            food = ExperimentalFood(**item)
        else:
            print(f"Unexpected DataType: {item['data_type']}")
        return food
