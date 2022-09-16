class Participant:
    def __init__(self, obj_id: int, first_name: str, second_name: str, weight: int = 1):
        self.id = obj_id
        self.first_name = first_name
        self.second_name = second_name
        self.weight = int(weight)

    def __str__(self) -> str:
        return f"{self.id} Name - {self.first_name} Second - {self.second_name} Weight - {self.weight}"


class Prize:
    def __init__(self, obj_id: int, name: str, amount: int = 1):
        self.id = obj_id
        self.name = name
        self.amount = amount

    def __str__(self):
        return f"{self.id} name - {self.name} amount - {self.amount}"
