import csv
import json
import pathlib
from typing import Generator, NamedTuple

from lottery.exceptions import LotteryError
from lottery.models import Participant

DEFAULT_DATA_FOLDER = 'data'
DEFAULT_PARTICIPANTS_FILE_NAME = 'participants2'
DEFAULT_PARTICIPANTS_FILE_SUFFIX = 'json'

INPUT_FORMATS = {
    'csv': lambda file: csv.DictReader(file),
    'json': lambda file: json.load(file)
}


class PathInput(NamedTuple):
    path: str
    name: str
    extension: str


def generate_participants(file_path, suffix) -> Generator[Participant, None, None]:
    if suffix not in INPUT_FORMATS:
        raise LotteryError("Not supported suffix")
    try:
        with open(file_path, mode='r') as file:
            try:
                for row in INPUT_FORMATS[suffix](file):
                    if 'first_name' not in row or 'last_name' not in row or 'id' not in row:
                        raise LotteryError("Error with loading data for file - wrong file schema")
                    elif 'weight' in row:
                        yield Participant(row['id'], row['first_name'], row['last_name'], row['weight'])
                    else:
                        yield Participant(row['id'], row['first_name'], row['last_name'])
            except ValueError:
                raise LotteryError("Error with loading data for file - cant read data")
    except OSError as e:
        raise LotteryError(f"Cant load data error - {e}") from e


def get_path_input() -> PathInput:
    path = input(f"Please enter the path to the data file [{DEFAULT_DATA_FOLDER}] - ")
    if not path:
        path = DEFAULT_DATA_FOLDER
    name = input(f"Name of the file [{DEFAULT_PARTICIPANTS_FILE_NAME}] - ")
    if not name:
        name = DEFAULT_PARTICIPANTS_FILE_NAME
    extension = input(
        f"Extension of the file (only json and csv are acceptable)[{DEFAULT_PARTICIPANTS_FILE_SUFFIX}] - "
    )
    if not extension:
        extension = DEFAULT_PARTICIPANTS_FILE_SUFFIX

    return PathInput(path, name, extension)


def load_participants() -> list[Participant]:

    path_from_input = get_path_input()

    file_path = pathlib.Path(__file__).parent.parent / path_from_input.path / (path_from_input.name + "." +
                                                                                    path_from_input.extension)

    data_gen = generate_participants(file_path, path_from_input[2])

    return list(data_gen)


def get_winners_count(participants_count: int) -> int:
    try:
        winner_count = int(input(f"How many winners you want to draw?({participants_count} max) - "))
    except ValueError:
        raise LotteryError("Winners count must be a number")
    if winner_count > participants_count or winner_count <= 0:
        raise LotteryError("Winners count must higher then  0 and smaller than amount of participants ")
    return winner_count
