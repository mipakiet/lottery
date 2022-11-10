import random

import pytest
from lottery.models import Participant, Prize
from lottery.app import Lottery
from faker import Faker


def participants_random(amount: int = 10) -> [Participant]:
    fake = Faker()
    name = fake.name().split(" ")
    return [Participant(x, name[0], name[1]) for x in range(amount)]


@pytest.fixture()
def participants(amount: int = 10) -> [Participant]:
    return participants_random(amount)


def prizes_random(amount: int = 5) -> [Prize]:
    result: [Prize] = []
    id_counter = 0
    fake = Faker()
    while amount > 0:
        amount_counter = fake.pyint(1, amount)
        result.append(Prize(id_counter, fake.color(), amount_counter))
        id_counter += 1
        amount -= amount_counter
    return result


@pytest.fixture()
def prizes(amount: int = 5) -> [Prize]:
    return prizes_random(amount)


@pytest.fixture()
def incomplete_participants():
    return '[{"id": "1", "last_name": "Bransgrove"}, {"id": "2", "last_name": "Spriggs"}]'


@pytest.fixture()
def incomplete_prizes():
    return '{"name": "Item giveaway: 5 identical prizes","prizes": [{"id": 1,"name": "Annual Vim subscription"}]}'


@pytest.fixture()
def lottery(participants_count: int = 10, prizes_count: int = 5) -> [Lottery]:
    lottery = Lottery(participants_random(participants_count), prizes_random(prizes_count))
    return lottery
