import pytest

from lottery.app import Lottery
from lottery.models import Participant, Prize

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

lottery1 = Lottery(participants1_Participant, prize1_Prize)


@pytest.mark.parametrize("lottery", [lottery1])
def test_draw_winners(lottery):
    lottery.draw_winners()

    assert len(lottery._Lottery__winners) == len(lottery._Lottery__prizes)

    for winner in lottery._Lottery__winners:
        assert winner in lottery._Lottery__participants

    # check if duplicates
    assert len(set([x for x in lottery._Lottery__winners if lottery._Lottery__winners.count(x) > 1])) == 0
