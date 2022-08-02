import random
from input_handling.get import load_participants, get_winners_count
from .extensions import LotteryError


def dashed_line():
    print('-' * 60)


class Lottery:
    def __init__(self):
        self.participant = []
        self.winner_count = None
        self.winners = []

    def draw_winners(self) -> None:
        self.winners = []
        participants_dict = {index: self.participant[index].weight for index in range(len(self.participant))}
        for i in range(self.winner_count):
            winner = random.choices(tuple(participants_dict), tuple(participants_dict.values()))[0]
            participants_dict.pop(winner)
            self.winners.append(self.participant[winner])

    def print_winners(self) -> None:
        print("The winners:")
        for winner in self.winners:
            print(f"{winner.first_name} {winner.second_name}")

    def run(self) -> None:

        dashed_line()
        print("HI! Welcome to the lottery!")
        dashed_line()

        try:
            self.participant = load_participants()
        except LotteryError as e:
            print(e)
            return

        dashed_line()

        try:
            self.winner_count = get_winners_count(len(self.participant))
        except LotteryError as e:
            print(e)
            return

        dashed_line()
        self.draw_winners()
        self.print_winners()
        dashed_line()
        print("Thx for using app!")
        dashed_line()
