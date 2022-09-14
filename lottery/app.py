import pathlib

import click
import random

from .get import get_first_prize_file, load_participants, load_prizes, generate_participants
from .exceptions import LotteryError
from .save import save_results
from .models import Participant, Prize


DEFAULT_DATA_FOLDER = 'data'
DEFAULT_PARTICIPANTS_FILE_NAME = 'participants1'
DEFAULT_PARTICIPANTS_FILE_SUFFIX = 'json'
DEFAULT_PRIZE_FOLDER = 'lottery_templates'


def draw_winners(participant: list[Participant], winner_count: int) -> list[Participant]:
    winners = []
    participants_dict = {index: participant[index].weight for index in range(len(participant))}
    for i in range(winner_count):
        winner = random.choices(tuple(participants_dict), participants_dict.values())[0]
        participants_dict.pop(winner)
        winners.append(participant[winner])

    return winners


def print_results(winners: list[Participant], prizes: list[Prize] = None) -> None:
    click.echo("The winners:")
    if prizes is None:
        for winner, prize in zip(winners, prizes):
            click.echo(f"{winner.first_name} {winner.second_name}({winner.id}) Prize - {prize.name}")
    else:
        for winner in winners:
            click.echo(f"{winner.first_name} {winner.second_name}({winner.id}) ")


@click.command()
@click.option('-datafile_path', prompt='Please enter path to the data file', default=DEFAULT_DATA_FOLDER,
              show_default=True)
@click.argument('datafile_name', default=DEFAULT_PARTICIPANTS_FILE_NAME)
@click.option('-datafile_suffix', prompt='Please enter suffix of the data file',
              default=DEFAULT_PARTICIPANTS_FILE_SUFFIX, show_default=True)
@click.argument('prize_file', default=get_first_prize_file(), type=str)
@click.option('-result_file', type=str)
def run(datafile_path, datafile_name, datafile_suffix, prize_file, result_file) -> None:
    try:
        participant = list(generate_participants(pathlib.Path(datafile_path) / (datafile_name + "." + datafile_suffix)))
    except LotteryError as e:
        click.echo(e)
        return

    try:
        prize = load_prizes(prize_file)
    except LotteryError as e:
        click.echo(e)
        return

    winner_count = len(prize)

    winners = draw_winners(participant, winner_count)

    if result_file:
        try:
            save_results(winners, prize, result_file)
        except LotteryError as e:
            click.echo(e)
            return
    else:
        print_results(winners, prize)

    click.echo("Thx for using app!")
