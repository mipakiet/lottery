import pathlib
import json
import csv
from lottery.models import *
from .validate import *

default_data_folder = 'data'
default_participants_file_name = 'participants2'
default_participants_file_extension = 'json'


def load_participants() -> list:

    path = input(f"Please enter the path to the data file [{default_data_folder}] - ")
    if not path:
        path = default_data_folder
    name = input(f"Name of the file [{default_participants_file_name}] - ")
    if not name:
        name = default_participants_file_name
    extension = input(
        f"Extension of the file (only json and csv are acceptable)[{default_participants_file_extension}] - "
    )
    if not extension:
        extension = default_participants_file_extension

    file_path = pathlib.Path().resolve() / path / (name + "." + extension)

    try:
        with open(file_path, mode='r') as file:
            if file_path.suffix == ".csv":
                data = csv.DictReader(file)
            elif file_path.suffix == ".json":
                data = json.load(file)
    except FileNotFoundError:
        raise FileNotFoundError("You entered wrong path")

    check_participants_data(data)

    result = []
    for item in data:
        if 'weight' in item:
            result.append(Participant(
                item['first_name'], item['last_name'], item['weight']))
        else:
            result.append(Participant(
                item['first_name'], item['last_name']))

    return result


def get_winners_count(participants_count: int) -> int:
    try:
        winner_count = int(input(f"How many winners you want to draw?({participants_count} max) - "))
    except ValueError:
        raise ValueError("Winners count must be a number")
    if winner_count > participants_count or winner_count <= 0:
        raise ValueError("Winners count must higher then  0 and smaller than amount of participants ")
    return winner_count
