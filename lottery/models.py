from dataclasses import dataclass


@dataclass
class Participant:
    id: int
    first_name: str
    last_name: str
    weight: int = 1

    def __str__(self) -> str:
        return f"{self.id} Name - {self.first_name} Second - {self.last_name} Weight - {self.weight}"


@dataclass
class Prize:
    id: int
    name: str
    amount: int = 1

    def __str__(self):
        return f"{self.id} name - {self.name} amount - {self.amount}"
