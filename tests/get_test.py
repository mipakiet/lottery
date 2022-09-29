import pytest
import pathlib
from click.testing import CliRunner
from unittest.mock import patch


from lottery.get import generate_participants, generate_prizes, get_first_prize_file, load_participants, load_prizes
from lottery.models import Participant, Prize
from lottery.exceptions import LotteryError

participants1 = [
    (1, "Tanny", "Bransgrove"),
    (2, "Delila", "Spriggs"),
    (3, "Sigmund", "Saw"),
    (4, "Wilt", "Maycey"),
    (5, "Carilyn", "Semper"),
    (6, "Rowland", "Heaysman"),
    (7, "Nev", "Driver"),
    (8, "Calypso", "Nursey"),
    (9, "Willow", "Tollemache"),
    (10, "Nert", "Hartell"),
]
participants1_Participant = [Participant(person[0], person[1], person[2]) for person in participants1]

prize1 = [
    {
      "id": 1,
      "name": "Gold medal",
      "amount": 1
    },
    {
      "id": 2,
      "name": "Silver medal",
      "amount": 1
    },
    {
      "id": 3,
      "name": "Bronze medal",
      "amount": 1
    }
]
prize1_Prize = [Prize(prize["id"], prize["name"], prize["amount"]) for prize in prize1]


def generate_participants1():
    for person in participants1_Participant:
        yield person


def generate_prizes1():
    for prize in prize1_Prize:
        yield prize


@pytest.mark.parametrize("file_path", [
    pathlib.Path('data_testing/participants1.csv'),
    pathlib.Path('data_testing/participants1.json'),
])
def test_generate_participants_success(file_path):
    gen = generate_participants(file_path)

    for item in gen:
        assert type(item) is Participant


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


@patch('lottery.get.generate_participants')
@pytest.mark.parametrize("file_path", [
    "data_testing/participants1.csv",
    "data_testing/participants1.json"
])
def test_load_participants(mock, file_path):
    mock.return_value = generate_participants1()
    result = load_participants(file_path)

    assert result == participants1_Participant


@patch('lottery.get.generate_prizes')
@pytest.mark.parametrize("file_path", [
    "data_testing/prize1.json",
])
def test_load_prizes(mock, file_path):
    mock.return_value = generate_prizes1()
    result = load_prizes(file_path)

    assert result == prize1_Prize
