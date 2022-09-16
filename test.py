import pytest
import pathlib

from lottery.get import generate_participants
from lottery.models import Participant
from lottery.exceptions import LotteryError


@pytest.mark.parametrize("file_path, suffix, expected", [
    ('data/participants1.csv', 'csv', Participant),
    ('data/participants1.json', 'json', Participant),
    ('data/participants.pdf', 'pdf', LotteryError),
    ('nopath', 'pdf', LotteryError),
])
def test_generate_participants_loading_data(file_path, suffix, expected):
    gen = generate_participants(pathlib.Path(file_path))

    if issubclass(expected, Exception):
        with pytest.raises(LotteryError):
            next(gen)
    else:
        for item in gen:
            assert type(item) is expected
