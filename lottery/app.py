import random
import pathlib
import json
import csv


class Participant:
    def __init__(self, first_name: str, second_name: str, weight=1):
        self.first_name = first_name
        self.second_name = second_name
        self.weight = weight

    def print_info(self):
        print(f"Name - {self.first_name} Second - {self.second_name} Weight - {self.weight}")


class Prize:
    pass


class Lottery:
    def __init__(self):
        self.participant = []

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
            extension = input("Extension of the file[only json and csv are acceptable][json] - ")
            if extension == "":
                extension = 'json'
            while extension not in ['csv', 'json']:
                print("Wrong extension")
                extension = input("Extension of the file[only json and csv are acceptable][json] - ")
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
                            print("Error with loading data from file - not enough columns")
                            return False
                        if len(row) > 3:
                            try:
                                weight = int(row[3])
                            except ValueError:
                                print("Error with loading data from file - weight must be integer")
                                return False
                            self.participant.append(Participant(row[1], row[2], weight))
                        else:
                            self.participant.append(Participant(row[1], row[2]))

                    line_count += 1
        elif file.suffix == ".json":
            with open(file, 'r') as f:
                data = json.load(f)
                for item in data:
                    if 'first_name' not in item and 'second_name' not in item:
                        print("Error with loading data from file - wrong variables names")
                        return False
                    if 'weight' in item:
                        self.participant.append(Participant(item['first_name'], item['last_name'], item['weight']))
                    else:
                        self.participant.append(Participant(item['first_name'], item['last_name']))

    def run(self):
        print('-' * 60)
        print("HI! Welcome to the lottery!")
        print('-' * 60)
        if not self.load_participants():
            return False
            return False

