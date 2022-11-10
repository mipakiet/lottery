import pathlib

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
    with patch("builtins.open") as open_mock:
        open_mock.side_effect = OSError
        with pytest.raises(LotteryError):
            lottery.save_results("test.json")


@patch("lottery.app.Lottery.print_results")
@patch("lottery.app.Lottery.save_results")
@patch("lottery.app.Lottery.draw_winners")
@patch("lottery.app.load_prizes")
@patch("lottery.app.generate_participants")
@patch("lottery.app.get_first_prize_file")
@pytest.mark.parametrize("arguments", [
    (['-datafile_path', 'datafile_path', 'datafile_name', '-datafile_suffix', 'datafile_suffix', 'prize_file',
      '-result_file', 'result_file'],
     [pathlib.Path("datafile_path") / "datafile_name.datafile_suffix", "prize_file", "result_file", False]),
    (['-datafile_path', 'datafile_path', 'datafile_name', '-datafile_suffix', 'datafile_suffix', 'prize_file'],
     [pathlib.Path("datafile_path") / "datafile_name.datafile_suffix", "prize_file", None, True]),
    (['-datafile_path', 'datafile_path', 'datafile_name', '-datafile_suffix', 'datafile_suffix'],
     [pathlib.Path("datafile_path") / "datafile_name.datafile_suffix", "prize_file", None, True]),
    (['-datafile_path', 'datafile_path', 'datafile_name'],
     [pathlib.Path("datafile_path") / "datafile_name.json", "prize_file", None, True]),
    ([],
     [pathlib.Path("data") / "participants1.json", "prize_file", None, True]),
])
def test_run(get_first_prize_file_mock, generate_participants_mock, load_prizes_mock, draw_winners_mock,
             save_results_mock, print_results_mock, arguments):
    get_first_prize_file_mock.return_value = arguments[1][1]

    runner = CliRunner()
    with LogCapture() as captured:
        result = runner.invoke(run, arguments[0])

    assert result.exit_code == 0
    assert generate_participants_mock.call_args.args[0] == arguments[1][0]
    assert load_prizes_mock.call_args.args[0] == arguments[1][1]
    assert draw_winners_mock.called is True
    if arguments[1][2] is None:
        assert save_results_mock.called is False
    else:
        assert save_results_mock.call_args.args[0] == arguments[1][2]
    assert print_results_mock.called is arguments[1][3]

    assert captured.records[0].getMessage() == "Thx for using app!"


@patch("lottery.app.generate_participants")
def test_run_load_prizes_exceptions(generate_participants_mock):
    runner = CliRunner()
    generate_participants_mock.side_effect = LotteryError
    with LogCapture() as captured:
        result = runner.invoke(run, ['-datafile_path', 'test', 'test', 'test', '-datafile_suffix', 'test',
                                     '-result_file', 'test'])
        assert "" == captured.records[0].getMessage()


@patch("lottery.app.load_prizes")
@patch("lottery.app.generate_participants")
def test_run__load_prize_exceptions(generate_participants_mock, load_prizes_mock):
    runner = CliRunner()
    generate_participants_mock.side_effect = None
    load_prizes_mock.side_effect = LotteryError
    with LogCapture() as captured:
        result = runner.invoke(run, ['-datafile_path', 'test1', 'test2', 'test3', '-datafile_suffix', 'test4',
                                     '-result_file', 'test5'])
        assert "" == captured.records[0].getMessage()
