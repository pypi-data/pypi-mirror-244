from .AbridgedFoodNutrient import AbridgedFoodNutrient
from .Food import Food
from datetime import datetime
from dataclasses import dataclass


@dataclass()
class AbridgedFood(Food):
    def __init__(self, fdc_id: int, data_type: str, description: str, publication_date: str = None,
                 food_nutrients: dict = None, ndb_number: int = None, brand_owner: str = None, gtin_upc: str = None,
                 food_code: str = None):
        """
        Abridged Food Object
        :param fdc_id: This is the number provided for each food data record in FoodData Central. A food record is the
        totality of information (e.g., values for components, including nutrients, descriptive information) published
        on a food item. Each time the data in a food record changes, that food item receives a new FDC_ID number.
        :param data_type: Type of Data, example: Branded
        :param description: Description of `AbridgedFood`
        :param publication_date: Date of Publication, converted to `datetime.date` object
        :param food_nutrients: Food Nutrient, converted to `AbridgedFoodNutrient` object
        :param ndb_number: This number is a unique identifier for each food in a specific form used for Foundation Foods
        and SR Legacy. Even if the FDC_ID number changes because of an update to the food record, the NDB number will
        remain the same because it is linked to the food, not to the information about the food. Users can search for
        a food item by the name of the food or the NDB number. Converted to `int`
        :param brand_owner: Name of Brand, only applies to Branded Foods
        :param gtin_upc: The GTIN is a number that can be used by a company to uniquely identify their trade items.
        It is used to identify specific food product in the USDA Global Branded Foods Database. Users can search for a
        specific food product by the name of the food or the GTIN number. More information on product identification
        can be found in Branded Food data quality documentation at https://fdc.nal.usda.gov/data-documentation.html .
        Only applies to Branded Foods
        :param food_code: An 8-digit number that identifies foods in FNDDS. These foods are used in analyses of NHANES
        dietary data. Users can search for a food in FNDDS either by its name or its food code. Only applies to
        Survey Foods
        """
        super().__init__()
        self.fdc_id = fdc_id
        self.description = description
        # Just using the if statements to avoid NoneType exceptions
        self.publication_date = datetime.strptime(publication_date,
                                                  "%Y-%m-%d").date() if publication_date else publication_date
        self.food_nutrients = [AbridgedFoodNutrient(**food_nutrient) for food_nutrient in
                               food_nutrients] if food_nutrients else food_nutrients
        self.data_type = data_type
        self.ndb_number = ndb_number
        self.brand_owner = brand_owner
        self.gtin_upc = gtin_upc
        self.food_code = food_code
