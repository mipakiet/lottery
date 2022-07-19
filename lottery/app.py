import random
import pathlib
import json
import csv


class Participant:
    def __init__(self, first_name, second_name, weight=1):
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
        def get_file_path():
            path = input("Please enter the path to the data file [data/] - ")
            if path == "":
                path = "data/"
            name = input("Name of the file [participants1] - ")
            if name == "":
                name = 'participants1'
            extension = input("Extension of the file[only json and csv are acceptable][csv] - ")
            if extension == "":
                extension = 'csv'
            while extension not in ["csv", "json"]:
                print("Wrong extension")
                extension = input("Extension of the file[only json and csv are acceptable] - ")

            file_direction = path + name + '.' + extension
            return pathlib.Path(file_direction)

        file = get_file_path()
        while not file.exists():
            print("File not exist. Let's try again")
            get_file_path()

        if file.suffix == ".csv":
            with open(file, mode='r') as csv_file:
                csv_reader = csv.reader(csv_file, delimiter=',')
                line_count = 0
                for row in csv_reader:
                    if line_count != 0:
                        if len(row) < 3:
                            print("Wrong csv format for this app")
                            return False
                        if len(row) > 3:
                            try:
                                weight = int(row[3])
                            except ValueError:
                                print("Wrong csv format for this app")
                                return False
                            self.participant.append(Participant(row[1], row[2], weight))
                        else:
                            self.participant.append(Participant(row[1], row[2]))

                    line_count += 1


    def run(self):
        print("HI! Welcome to the lottery!")
        self.load_participants()
