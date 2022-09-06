import click
import random

from .get import load_participants, load_prizes, get_results_files_path
from .exceptions import LotteryError
from .save import save_results


def dashed_line():
    click.echo('-' * 100)


class Lottery:
    def __init__(self):
        self.participant = []
        self.prize =[]
        self.winner_count = None
        self.winners = []

    def draw_winners(self) -> None:
        self.winners = []
        participants_dict = {index: self.participant[index].weight for index in range(len(self.participant))}
        for i in range(self.winner_count):
            winner = random.choices(tuple(participants_dict), participants_dict.values())[0]
            participants_dict.pop(winner)
            self.winners.append(self.participant[winner])

    def print_results(self, prizes: bool = None) -> None:
        click.echo("The winners:")
        if prizes:
            for winner, prize in zip(self.winners, self.prize):
                click.echo(f"{winner.first_name} {winner.second_name}({winner.id}) Prize - {prize.name}")
        else:
            for winner in self.winners:
                click.echo(f"{winner.first_name} {winner.second_name}({winner.id}) ")

    def run(self) -> None:
        dashed_line()
        click.echo("HI! Welcome to the lottery!")

        dashed_line()
        try:
            click.echo("Participants file")
            self.participant = load_participants()
        except LotteryError as e:
            click.echo(e)
            return

        dashed_line()
        try:
            click.echo("Prizes file")
            self.prize = load_prizes()
        except LotteryError as e:
            click.echo(e)
            return

        # try:
        #     self.winner_count = get_winners_count(len(self.participant))
        # except LotteryError as e:
        #     click.echo(e)
        #     return
        self.winner_count = len(self.prize)

        dashed_line()
        self.draw_winners()
        self.print_results(prizes=True)

        dashed_line()
        if click.confirm(f"Do you want save results?"):
            save_path = get_results_files_path()
            try:
                save_results(self.winners, self.prize, save_path)
            except LotteryError as e:
                click.echo(e)
                return

        dashed_line()
        click.echo("Thx for using app!")
