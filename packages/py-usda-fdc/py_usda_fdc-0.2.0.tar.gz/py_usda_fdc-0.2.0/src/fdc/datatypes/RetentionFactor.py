from dataclasses import dataclass


@dataclass()
class RetentionFactor:
    def __init__(self, id: int = None, code: int = None, description: str = None):
        self.id = id
        self.code = code
        self.description = description
