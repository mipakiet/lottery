import random
from input_handling.get import *


def dashed_line():
    print('-' * 60)


class Lottery:
    def __init__(self):
        self.participant = []
        self.winner_count = None
        self.winners = []

    def draw_winners(self) -> None:
        participant = self.participant.copy()
        for i in range(self.winner_count):
            winner = random.choices(participant, weights=[x.weight for x in participant])[0]
            participant.remove(winner)
            self.winners.append(winner)

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
        except DataError as e:
            print(e)
            return
        except FileNotFoundError as e:
            print(e)
            return

        dashed_line()

        try:
            self.winner_count = get_winners_count(len(self.participant))
        except ValueError as e:
            print(e)
            return

        dashed_line()
        self.draw_winners()
        self.print_winners()
        dashed_line()
        print("Thx for using app!")
        dashed_line()
