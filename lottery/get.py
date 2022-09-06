import csv
import click
import json
import pathlib
from typing import Generator

from lottery.exceptions import LotteryError
from lottery.models import Participant, Prize

DEFAULT_DATA_FOLDER = 'data'
DEFAULT_PARTICIPANTS_FILE_NAME = 'participants1'
DEFAULT_PARTICIPANTS_FILE_SUFFIX = 'json'
DEFAULT_PRIZE_FOLDER = 'lottery_templates'

PARTICIPANTS_INPUT_FORMATS = {
    'csv': lambda file: csv.DictReader(file),
    'json': lambda file: json.load(file),
}

PRIZE_INPUT_FORMATS = {
    'json': lambda file: json.load(file),
}

# class PathInput(NamedTuple):
#     path: str
#     name: str
#     suffix: str


def generate_participants(file_path) -> Generator[Participant, None, None]:
    suffix = file_path.suffix[1:]
    if suffix not in PARTICIPANTS_INPUT_FORMATS:
        raise LotteryError("Not supported suffix")
    try:
        with open(file_path, mode='r') as file:
            try:
                for row in PARTICIPANTS_INPUT_FORMATS[suffix](file):
                    if 'id' not in row or 'first_name' not in row or 'last_name' not in row:
                        raise LotteryError("Error with loading data for file - wrong file schema")
                    elif 'weight' in row:
                        yield Participant(row['id'], row['first_name'], row['last_name'], row['weight'])
                    else:
                        yield Participant(row['id'], row['first_name'], row['last_name'])
            except ValueError:
                raise LotteryError("Error with loading data for file - cant read data")
    except OSError as e:
        raise LotteryError(f"Cant load data error - {e}") from e


def generate_prizes(file_path) -> Generator[Prize, None, None]:
    suffix = file_path.suffix[1:]
    if suffix not in PRIZE_INPUT_FORMATS:
        raise LotteryError("Not supported suffix")
    try:
        with open(file_path, mode='r') as file:
            try:
                for row in PRIZE_INPUT_FORMATS[suffix](file)['prizes']:
                    if 'id' not in row or 'name' not in row or 'amount' not in row:
                        raise LotteryError("Error with loading data for file - wrong file schema")
                    else:
                        yield Prize(row['id'], row['name'], row['amount'])
            except ValueError:
                raise LotteryError("Error with loading data for file - cant read data")
    except OSError as e:
        raise LotteryError(f"Cant load data error - {e}") from e


def get_participants_file_path() -> pathlib.Path:
    folder_path = click.prompt("Please enter the path to the data file", type=str, default=DEFAULT_DATA_FOLDER,
                               show_default=True)
    name = click.prompt("Name of the file", type=str, default=DEFAULT_PARTICIPANTS_FILE_NAME, show_default=True)
    suffix = click.prompt("Extension of the file", type=click.Choice(PARTICIPANTS_INPUT_FORMATS.keys()),
                          default=DEFAULT_PARTICIPANTS_FILE_SUFFIX, show_default=True)
    return pathlib.Path(__file__).parent.parent / folder_path / (name + "." + suffix)


def get_prize_file_path() -> pathlib.Path:
    prizes_path = pathlib.Path(__file__).parent.parent / DEFAULT_DATA_FOLDER / DEFAULT_PRIZE_FOLDER
    first_file = next(prizes_path.glob('**/*'))
    first_file_user_friendly_string = str(first_file)[str(first_file).find(DEFAULT_DATA_FOLDER)::]
    if click.confirm(f"Do you want load prizes from \"{first_file_user_friendly_string}\"?"):
        return first_file
    else:
        folder_path = click.prompt("Please enter the path to the prize file", type=str)
        name = click.prompt("Name of the file", type=str)
        suffix = click.prompt("Extension of the file", type=click.Choice(PRIZE_INPUT_FORMATS.keys()))
        path = pathlib.Path(__file__).parent.parent / folder_path / (name + "." + suffix)
        return path


def get_results_files_path() -> pathlib.Path:
    folder_path = click.prompt("Please enter the path to the results file", type=str)
    name = click.prompt("Name of the file (will be saved in json format)", type=str)
    return pathlib.Path(folder_path) / (name + "." + "json")


def load_participants() -> list[Participant]:
    file_path = get_participants_file_path()
    data_gen = generate_participants(file_path)

    return list(data_gen)


def load_prizes() -> list[Prize]:
    file_path = get_prize_file_path()
    data_gen = generate_prizes(file_path)

    return list(data_gen)


def get_winners_count(participants_count: int) -> int:
    winner_count = click.prompt("How many winners you want to draw?", type=click.IntRange(1, participants_count))
    return winner_count
