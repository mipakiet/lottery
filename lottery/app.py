import pathlib
import logging
import click
import random

from .get import get_first_prize_file, load_prizes, generate_participants
from .exceptions import LotteryError
from .save import save_results
from .models import Participant, Prize
from dataclasses import dataclass


DEFAULT_DATA_FOLDER = 'data'
DEFAULT_PARTICIPANTS_FILE_NAME = 'participants1'
DEFAULT_PARTICIPANTS_FILE_SUFFIX = 'json'
DEFAULT_PRIZE_FOLDER = 'lottery_templates'


@dataclass
class Lottery:
    participants: list[Participant]
    prizes: list[Prize]

    def print_results(self, winners: list[Participant]) -> None:
        logging.info("The winners:")
        for winner, prize in zip(winners, self.prizes):
            logging.info(f"{winner.first_name} {winner.second_name}({winner.id}) Prize - {prize.name}")

    def draw_winners(self) -> list[Participant]:
        participants_dict = {index: self.participants[index].weight for index in range(len(self.participants))}
        winners = []
        for i in range(len(self.prizes)):
            winner = random.choices(tuple(participants_dict), participants_dict.values())[0]
            participants_dict.pop(winner)
            winners.append(self.participants[winner])
        return winners


@click.command()
@click.option('-datafile_path', prompt='Please enter path to the data file', default=DEFAULT_DATA_FOLDER,
              show_default=True)
@click.argument('datafile_name', default=DEFAULT_PARTICIPANTS_FILE_NAME)
@click.option('-datafile_suffix', prompt='Please enter suffix of the data file',
              default=DEFAULT_PARTICIPANTS_FILE_SUFFIX, show_default=True)
@click.argument('prize_file', default=get_first_prize_file(DEFAULT_DATA_FOLDER, DEFAULT_PRIZE_FOLDER), type=str)
@click.option('-result_file', type=str)
def run(datafile_path, datafile_name, datafile_suffix, prize_file, result_file) -> None:

    try:
        participant = list(generate_participants(pathlib.Path(datafile_path) / (datafile_name + "." + datafile_suffix)))
    except LotteryError as e:
        logging.info(e)
        return

    try:
        prize = load_prizes(prize_file)
    except LotteryError as e:
        logging.info(e)
        return

    lottery = Lottery(participant, prize)
    winners = lottery.draw_winners()

    if result_file:
        try:
            save_results(winners, lottery.prizes, result_file)
        except LotteryError as e:
            logging.info(e)
            return
    else:
        lottery.print_results(winners)

    logging.info("Thx for using app!")

