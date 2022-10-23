import csv
import json
import pathlib
from typing import Generator

from lottery.exceptions import LotteryError
from lottery.models import Participant, Prize


PARTICIPANTS_INPUT_FORMATS = {
    'csv': lambda file: csv.DictReader(file),
    'json': lambda file: json.load(file),
}

PRIZE_INPUT_FORMATS = {
    'json': lambda file: json.load(file),
}


def generate_participants(file_path: pathlib.Path) -> Generator[Participant, None, None]:
    suffix = file_path.suffix[1:]
    if suffix not in PARTICIPANTS_INPUT_FORMATS:
        raise LotteryError("Not supported suffix")
    try:
        with open(file_path, mode='r') as file:
            try:
                for row in PARTICIPANTS_INPUT_FORMATS[suffix](file):
                    if 'id' not in row or 'first_name' not in row or 'last_name' not in row:
                        raise LotteryError("Error with loading data for file - wrong file schema")
                    yield Participant(row['id'], row['first_name'], row['last_name'], row.get('weight', 1))
            except ValueError:
                raise LotteryError("Error with loading data for file - cant read data")
    except OSError as e:
        raise LotteryError(f"Cant load data error - {e}") from e


def generate_prizes(file_path: pathlib.Path) -> Generator[Prize, None, None]:
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


def get_first_prize_file(data_folder, prize_folder) -> str:
    prizes_path = pathlib.Path(__file__).parent.parent / data_folder / prize_folder
    try:
        first_file = next(prizes_path.glob('**/*'))
    except StopIteration:
        raise LotteryError("There is no prize file")
    first_file_user_friendly_string = first_file.relative_to(prizes_path.parent.parent)
    return str(first_file_user_friendly_string)


def load_prizes(file_path_str: str) -> list[Prize]:
    file_path = pathlib.Path(file_path_str)
    data_gen = generate_prizes(file_path)

    return list(data_gen)
