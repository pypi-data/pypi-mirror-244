from src.fdc.datatypes import *


class TestDataclass:
    tmp = {"fdc_id": 1, "data_type": "AbridgedFood", "description": "test_food", "publication_date": "2023-09-01",
           "food_nutrients": None, "ndb_number": 1, "brand_owner": "Kraft", "gtin_upc": None, "food_code": None}

    def test_abridged_equals(self):
        x = AbridgedFood(**self.tmp)
        y = AbridgedFood(**self.tmp)
        assert x == y

    def test_repr(self):
        x = AbridgedFood(**self.tmp).__repr__()
        assert "AbridgedFood()" == x
