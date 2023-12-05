from dataclasses import dataclass


@dataclass()
class MeasureUnit:
    def __init__(self, id: int = None, abbreviation: str = None, name: str = None):
        self.id = id
        self.abbreviation = abbreviation
        self.name = name
