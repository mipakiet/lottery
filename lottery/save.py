import pathlib
import json

from lottery.models import Participant, Prize
from lottery.exceptions import LotteryError


def save_results(participants: list[Participant], prizes: list[Prize], path_file_dtr: str):
    path_file = pathlib.Path(path_file_dtr)
    try:
        with open(path_file, mode='w') as json_file:
            for winner, prize in zip(participants, prizes):
                row = {"first_name": winner.first_name, "last_name": winner.second_name, "participant_id": winner.id,
                       "prize": prize.name}
                json.dump(row, json_file)
    except OSError as e:
        raise LotteryError(f"Cant save results {e}") from e


