import pytest
import pathlib
from click.testing import CliRunner

from lottery.get import generate_participants, generate_prizes
from lottery.models import Participant, Prize
from lottery.exceptions import LotteryError


@pytest.mark.parametrize("file_path, expected", [
    (pathlib.Path('data_testing/participants1.csv'), Participant),
    (pathlib.Path('data_testing/participants1.json'), Participant),
    (pathlib.Path('data_testing/participants.pdf'), LotteryError),
    (pathlib.Path('data_testing/participants-broken.json'), LotteryError),
    (pathlib.Path('nofile'), LotteryError),
    (pathlib.Path('C:\\somefile.json'), LotteryError),
])
def test_generate_participants_loading_data(file_path, expected):
    gen = generate_participants(file_path)

    if issubclass(expected, Exception):
        with pytest.raises(LotteryError):
            next(gen)
    else:
        for item in gen:
            assert type(item) is expected


@pytest.mark.parametrize("file_path, expected", [
    (pathlib.Path('data_testing/lottery_templates/prize1.json'), Prize),
    (pathlib.Path('data_testing/lottery_templates/prize2.json'), Prize),
    (pathlib.Path('data_testing/lottery_templates/prize1.pdf'), LotteryError),
    (pathlib.Path('data_testing/lottery_templates/prize-broken.json'), LotteryError),
    (pathlib.Path('data_testing/lottery_templates/nofile.pdf'), LotteryError),
    (pathlib.Path('C:\\somefile.json'), LotteryError),
])
def test_generate_prizes_loading_data(file_path, expected):
    gen = generate_prizes(file_path)

    if issubclass(expected, Exception):
        with pytest.raises(LotteryError):
            next(gen)
    else:
        for item in gen:
            assert type(item) is expected


def test_load_participants(mocker):
    pass