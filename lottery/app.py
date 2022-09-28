import pathlib
import logging
import click
import random
import json

from .get import get_first_prize_file, load_prizes, generate_participants
from .exceptions import LotteryError
from .models import Participant, Prize


DEFAULT_DATA_FOLDER = 'data'
DEFAULT_PARTICIPANTS_FILE_NAME = 'participants1'
DEFAULT_PARTICIPANTS_FILE_SUFFIX = 'json'
DEFAULT_PRIZE_FOLDER = 'lottery_templates'


class Lottery:

    def __init__(self, participants:  list[Participant], prizes: list[Prize]):
        self.__participants = participants
        self.__prizes = prizes
        self.__winners: list[Participant] | None = None

    def draw_winners(self) -> None:
        participants_dict = {index: self.__participants[index].weight for index in range(len(self.__participants))}
        self.__winners = []
        for i in range(len(self.__prizes)):
            winner = random.choices(tuple(participants_dict), participants_dict.values())[0]
            participants_dict.pop(winner)
            self.__winners.append(self.__participants[winner])

    def print_results(self) -> None:
        if self.__winners is None:
            raise LotteryError("You have to draw winners ")
        logging.info("The winners:")
        for winner, prize in zip(self.__winners, self.__prizes):
            logging.info(f"{winner.first_name} {winner.second_name}({winner.id}) Prize - {prize.name}")

    def save_results(self, path_file_dtr: str) -> None:
        if self.__winners is None:
            raise LotteryError("You have to draw winners ")
        path_file = pathlib.Path(path_file_dtr)
        result = []
        for winner, prize in zip(self.__winners, self.__prizes):
            result.append(
                {"first_name": winner.first_name, "last_name": winner.second_name, "participant_id": winner.id,
                 "prize": prize.name})
        try:
            with open(path_file, mode='w') as json_file:
                json.dump(result, json_file)
        except OSError as e:
            raise LotteryError(f"Cant save results {e}") from e


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
    lottery.draw_winners()

    if result_file:
        lottery.save_results(result_file)
    else:
        lottery.print_results()

    logging.info("Thx for using app!")

