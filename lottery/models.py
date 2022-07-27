class Participant:
    def __init__(self, first_name: str, second_name: str, weight: int = 1):
        self.first_name = first_name
        self.second_name = second_name
        self.weight = int(weight)

    def __str__(self) -> str:
        return f"Name - {self.first_name} Second - {self.second_name} Weight - {self.weight}"


class Prize:
    pass
