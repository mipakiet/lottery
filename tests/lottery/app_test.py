import mock
import pytest
from unittest.mock import patch
from testfixtures import LogCapture
import random
from click.testing import CliRunner

from lottery.app import Lottery, run
from lottery.exceptions import LotteryError


@pytest.mark.parametrize("lottery", [(30, 1), (20, 10), (5, 5), (1, 1)], indirect=True)
def test_draw_winners(lottery: Lottery):
    winners = 0
    for prize in lottery._Lottery__prizes:
        winners += prize.amount
    participants_count = len(lottery._Lottery__participants)
    winners_indexes = [[x] for x in random.sample(range(0, participants_count), winners)]
    result = [lottery._Lottery__participants[x[0]] for x in winners_indexes]
    with patch("random.choices", side_effect=winners_indexes):
        lottery.draw_winners()
    assert lottery._Lottery__winners == result


def test_print_results(lottery):
    lottery.draw_winners()
    with LogCapture() as captured:
        lottery.print_results()
    winners = lottery._Lottery__winners
    prizes = lottery._Lottery__prizes
    prizes_name_list = []
    for prize in prizes:
        for _ in range(prize.amount):
            prizes_name_list.append(prize.name)
    for index in range(len(winners)):
        assert captured.records[index+1].getMessage() == f"{winners[index].first_name} {winners[index].last_name}" \
                                                       f"({winners[index].id}) Prize - {prizes_name_list[index]}"


def test_print_results_no_winners(lottery):
    with pytest.raises(LotteryError):
        lottery.print_results()


def test_save_results(mocker, lottery):
    mocker.patch("builtins.open")
    lottery.draw_winners()
    with patch('json.dump') as mocked_data:
        lottery.save_results("test.json")
        result = mocked_data.call_args[0][0]

    winners = lottery._Lottery__winners
    prizes = lottery._Lottery__prizes
    prizes_name_list = []
    for prize in prizes:
        for _ in range(prize.amount):
            prizes_name_list.append(prize.name)
    for index in range(len(winners)):
        assert result[index] == {"first_name": winners[index].first_name, "last_name": winners[index].last_name,
                                 "participant_id": winners[index].id, "prize": prizes_name_list[index]}


def test_save_results_no_winners(lottery):
    with pytest.raises(LotteryError):
        lottery.save_results("test.json")


def test_save_results_broken_file(lottery):
    lottery.draw_winners()
    with mock.patch("builtins.open") as open_mock:
        open_mock.side_effect = OSError
        with pytest.raises(LotteryError):
            lottery.save_results("test.json")


@patch("lottery.app.Lottery.print_results")
@patch("lottery.app.Lottery.save_results")
@patch("lottery.app.Lottery.draw_winners")
@patch("lottery.app.load_prizes")
@patch("lottery.app.generate_participants")
def test_run(generate_participants_mock, load_prizes_mock, draw_winners_mock, save_results_mock, print_results_mock):
    runner = CliRunner()
    with LogCapture() as captured:
        result = runner.invoke(run, ['-datafile_path', 'test', 'test', 'test', '-datafile_suffix', 'test',
                                     '-result_file', 'test'])

    assert captured.records[0].getMessage() == "Thx for using app!"

    with LogCapture() as captured:
        runner.invoke(run, ['-datafile_path', 'test', 'test', 'test', '-datafile_suffix', 'test'])

    assert captured.records[0].getMessage() == "Thx for using app!"


@patch("lottery.app.load_prizes")
@patch("lottery.app.generate_participants")
def test_run_exceptions(generate_participants_mock, load_prizes_mock):
    runner = CliRunner()
    generate_participants_mock.side_effect = LotteryError
    with LogCapture() as captured:
        result = runner.invoke(run, ['-datafile_path', 'test', 'test', 'test', '-datafile_suffix', 'test',
                                     '-result_file', 'test'])
        assert "" == captured.records[0].getMessage()

    generate_participants_mock.side_effect = None
    load_prizes_mock.side_effect = LotteryError
    with LogCapture() as captured:
        result = runner.invoke(run, ['-datafile_path', 'test', 'test', 'test', '-datafile_suffix', 'test',
                                     '-result_file', 'test'])
        assert "" == captured.records[0].getMessage()
