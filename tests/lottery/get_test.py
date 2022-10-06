import pytest
import pathlib
from unittest.mock import patch, mock_open

from lottery.get import generate_participants, generate_prizes, get_first_prize_file, load_prizes
from lottery.models import Participant, Prize
from lottery.exceptions import LotteryError


@pytest.mark.parametrize("participants_random", [1, 5, 10, 100], indirect=True)
def test_generate_participants_success(participants_random):

    path = pathlib.Path("test.json")
    mocker = mock_open(read_data=str(participants_random))
    with patch('builtins.open', mocker):
        gen = generate_participants(path)
    assert list(gen) is participants_random


@pytest.mark.parametrize("file_path", [
    pathlib.Path('data_testing/participants.pdf'),
    pathlib.Path('data_testing/participants-broken.json'),
    pathlib.Path('nofile'),
    pathlib.Path('C:\\somefile.json'),
])
def test_generate_participants_exception(file_path):
    gen = generate_participants(file_path)

    with pytest.raises(LotteryError):
        next(gen)


@pytest.mark.parametrize("file_path", [
    pathlib.Path('data_testing/participants.pdf'),
    pathlib.Path('data_testing/participants-broken.json'),
    pathlib.Path('nofile'),
    pathlib.Path('C:\\somefile.json'),
])
def test_generate_participants_exception(file_path):
    gen = generate_participants(file_path)

    with pytest.raises(LotteryError):
        next(gen)


@pytest.mark.parametrize("file_path", [
    pathlib.Path('data_testing/lottery_templates/prize1.json'),
    pathlib.Path('data_testing/lottery_templates/prize2.json'),
])
def test_generate_prizes_success(file_path):
    gen = generate_prizes(file_path)

    for item in gen:
        assert type(item) is Prize


@pytest.mark.parametrize("file_path", [
    pathlib.Path('data_testing/lottery_templates/prize1.pdf'),
    pathlib.Path('data_testing/lottery_templates/prize-broken.json'),
    pathlib.Path('data_testing/lottery_templates/nofile.pdf'),
    pathlib.Path('C:\\somefile.json'),
])
def test_generate_prizes_exception(file_path):
    gen = generate_prizes(file_path)

    with pytest.raises(LotteryError):
        next(gen)


@pytest.mark.parametrize("data_folder, prize_folder, result", [
    ("tests\\data_testing", "lottery_templates", "data_testing\\lottery_templates\\a.json"),
])
def test_get_first_prize_file_success(data_folder, prize_folder, result):

    assert get_first_prize_file(data_folder, prize_folder) == result


@pytest.mark.parametrize("data_folder, prize_folder, result", [
    ("tests\\data_testing", "empty_folder", "data_testing\\empty_folder\\a.json"),
])
def test_get_first_prize_file_exception(data_folder, prize_folder, result):
    with pytest.raises(LotteryError):
        get_first_prize_file(data_folder, prize_folder)


def test_load_prizes(mock, file_path):
    mock.return_value = generate_prizes1()
    result = load_prizes(file_path)

    assert result == prize1_Prize
