import pytest
import pathlib
from unittest.mock import patch

from lottery.get import generate_participants, generate_prizes, get_first_prize_file, load_prizes
from lottery.models import Participant, Prize
from lottery.exceptions import LotteryError


@pytest.mark.parametrize("participants", [1, 5, 10, 100], indirect=True)
def test_generate_participants_success(participants: list[Participant], mocker):
    participants_data = str([x.__dict__ for x in participants]).replace("\'", "\"")
    mocked_data = mocker.mock_open(read_data=participants_data)
    mocker.patch("builtins.open", mocked_data)
    result = list(generate_participants(pathlib.Path("test.json")))
    assert result == participants


@pytest.mark.parametrize("file_path", [
    pathlib.Path('data_testing/participants.pdf'),
    pathlib.Path('data_testing/participants-broken.json'),
    pathlib.Path('nofile'),
    pathlib.Path('C:\\somefile.json'),
])
def test_generate_participants_exception_wrong_file(file_path):
    gen = generate_participants(file_path)

    with pytest.raises(LotteryError):
        next(gen)


def test_generate_participants_exception_broken_file(mocker):
    mocked_data = mocker.mock_open(read_data="BUM")
    mocker.patch("builtins.open", mocked_data)
    with pytest.raises(LotteryError):
        list(generate_participants(pathlib.Path("test.json")))


def test_generate_participants_exception_incomplete_data(incomplete_participants, mocker):
    mocked_data = mocker.mock_open(read_data=incomplete_participants)
    mocker.patch("builtins.open", mocked_data)
    with pytest.raises(LotteryError):
        list(generate_participants(pathlib.Path("test.json")))


@pytest.mark.parametrize("prizes", [1, 5, 10, 100], indirect=True)
def test_generate_prizes_success(prizes: list[Prize], mocker):
    prizes_data = str({"prizes": [x.__dict__ for x in prizes]}).replace("\'", "\"")
    mocked_data = mocker.mock_open(read_data=prizes_data)
    mocker.patch("builtins.open", mocked_data)
    result = list(generate_prizes(pathlib.Path("test.json")))
    assert result == prizes


@pytest.mark.parametrize("file_path", [
    pathlib.Path('data_testing/lottery_templates/prize1.pdf'),
    pathlib.Path('data_testing/lottery_templates/prize-broken.json'),
    pathlib.Path('data_testing/lottery_templates/nofile.pdf'),
    pathlib.Path('C:\\somefile.json'),
])
def test_generate_prizes_exception_wrong_file(file_path):
    gen = generate_prizes(file_path)

    with pytest.raises(LotteryError):
        next(gen)


def test_generate_prizes_exception_broken_file(mocker):
    mocked_data = mocker.mock_open(read_data="BUM")
    mocker.patch("builtins.open", mocked_data)
    with pytest.raises(LotteryError):
        list(generate_prizes(pathlib.Path("test.json")))


def test_generate_prizes_exception_incomplete_data(incomplete_prizes, mocker):
    mocked_data = mocker.mock_open(read_data=incomplete_prizes)
    mocker.patch("builtins.open", mocked_data)
    with pytest.raises(LotteryError):
        list(generate_prizes(pathlib.Path("test.json")))


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


@patch("lottery.get.generate_prizes")
@pytest.mark.parametrize("prizes", [1, 5, 10, 100], indirect=True)
def test_load_prizes(mock, prizes):
    mock.return_value = prizes
    result = load_prizes("test.json")

    assert result == prizes
