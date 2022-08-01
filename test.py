import unittest

from input_handling.get import get_generator
from lottery.models import Participant
from lottery.extensions import LotteryError


class TestInputHandling(unittest.TestCase):
    def test_get_generator(self):
        file_path = 'data/participants1.csv'
        suffix = 'csv'
        gen = get_generator(file_path, suffix)
        for item in gen:
            self.assertIsInstance(item, Participant)

        file_path = 'data/participants2.csv'
        suffix = 'csv'
        gen = get_generator(file_path, suffix)
        for item in gen:
            self.assertIsInstance(item, Participant)

        file_path = 'data/participants1.json'
        suffix = 'json'
        gen = get_generator(file_path, suffix)
        for item in gen:
            self.assertIsInstance(item, Participant)

        file_path = 'data/participants2.json'
        suffix = 'json'
        gen = get_generator(file_path, suffix)
        for item in gen:
            self.assertIsInstance(item, Participant)

        file_path = 'data/participants2.pdf'
        suffix = 'pdf'
        gen = get_generator(file_path, suffix)
        with self.assertRaises(LotteryError):
            next(gen)

        file_path = 'data/nopath'
        suffix = 'json'
        gen = get_generator(file_path, suffix)
        with self.assertRaises(LotteryError):
            next(gen)


if __name__ == '__main__':
    unittest.main()
