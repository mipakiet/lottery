import random
import pathlib
import json
import csv


class Participant:
    def __init__(self, first_name: str, second_name: str, weight=1):
        self.first_name = first_name
        self.second_name = second_name
        self.weight = int(weight)

    def print_info(self):
        print(
            f"Name - {self.first_name} Second - {self.second_name} Weight - {self.weight}")


class Prize:
    pass


class Lottery:
    def __init__(self):
        self.participant = []
        self.winner_count = None
        self.winners = None

    def load_participants(self):

        file = pathlib.Path()
        first_time = True

        while first_time or not file.exists():
            if first_time:
                first_time = False
            else:
                print("Wrong file path. Try again.")

            path = input("Please enter the path to the data file [data/] - ")
            if path == "":
                path = "data/"
            name = input("Name of the file [participants2] - ")
            if name == "":
                name = 'participants2'
            extension = input(
                "Extension of the file (only json and csv are acceptable)[json] - ")
            if extension == "":
                extension = 'json'
            while extension not in ['csv', 'json']:
                print("Wrong extension")
                extension = input(
                    "Extension of the file (only json and csv are acceptable)[json] - ")
                if extension == "":
                    extension = 'json'

            file_direction = path + name + '.' + extension
            file = pathlib.Path(file_direction)

        if file.suffix == ".csv":
            with open(file, mode='r') as csv_file:
                csv_reader = csv.reader(csv_file, delimiter=',')
                line_count = 0
                for row in csv_reader:
                    if line_count != 0:
                        if len(row) < 3:
                            print(
                                "Error with loading data from file - not enough columns")
                            exit()
                        if len(row) > 3:
                            try:
                                weight = int(row[3])
                            except ValueError:
                                print(
                                    "Error with loading data from file - weight must be integer")
                                exit()
                            self.participant.append(
                                Participant(row[1], row[2], weight))
                        else:
                            self.participant.append(
                                Participant(row[1], row[2]))

                    line_count += 1
        elif file.suffix == ".json":
            # nice to add checking json with jsonschema
            with open(file, 'r') as f:
                data = json.load(f)
                for item in data:
                    if 'first_name' not in item or 'last_name' not in item:
                        print(
                            "Error with loading data from file - there are no needed variables")
                        exit()
                    if 'weight' in item:
                        self.participant.append(Participant(
                            item['first_name'], item['last_name'], item['weight']))
                    else:
                        self.participant.append(Participant(
                            item['first_name'], item['last_name']))

    def get_winners_count(self):
        participants_count = len(self.participant)
        winner_count = input("How many winners you want to draw? - ")
        while not winner_count.isnumeric() or int(winner_count) > participants_count or int(winner_count) <= 0:
            print(
                f"Please enter the number lower than {participants_count + 1} and higher than 0")
            winner_count = input("How many winners you want to draw? - ")
        self.winner_count = int(winner_count)

    def draw_winners(self):
        # winners can be duplicated
        self.winners = random.choices(self.participant, weights=[x.weight for x in self.participant],
                                      k=self.winner_count)

    def print_winners(self):
        print("The winners:")
        for winner in self.winners:
            print(f"{winner.first_name} {winner.second_name}")

    def run(self):
        def dashed_line():
            print('-' * 60)

        dashed_line()
        print("HI! Welcome to the lottery!")
        dashed_line()
        self.load_participants()
        dashed_line()
        self.get_winners_count()
        dashed_line()
        self.draw_winners()
        self.print_winners()
        dashed_line()
        print("Thx for using app!")
        dashed_line()
