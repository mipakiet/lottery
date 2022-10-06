import pytest
from unittest.mock import patch
from testfixtures import LogCapture

from lottery.app import Lottery


@pytest.mark.parametrize("lottery", [(30, 5), (5, 5), (10, 3)], indirect=True)
def test_draw_winners(lottery: Lottery):
    winners = 0
    for prize in lottery._Lottery__prizes:
        winners += prize.amount
    result = [lottery._Lottery__participants[x] for x in range(winners)]
    with patch("random.choices", side_effect=result):
        lottery.draw_winners()
    assert lottery._Lottery__winners == result


def test_print_results(lottery):
    lottery.draw_winners()
    with LogCapture() as captured:
        lottery.print_results()
    winners = lottery._Lottery__winners
    prizes = lottery._Lottery__prizes
    for index in range(len(winners)):
        assert captured.records[index].getMessage() == f"{winners[index].first_name} {winners[index].second_name}" \
                                                       f"({winners[index].id}) Prize - {prizes[index].name} "

