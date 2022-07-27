
class DataError(Exception):
    pass


def check_participants_data(data: list) -> None:
    if not data:
        raise DataError("Empty data")

    for item in data:
        if 'first_name' not in item or 'last_name' not in item:
            raise DataError("Not required field")
        if 'weight' in item and not item['weight'].isnumeric():
            raise DataError("Wrong type of field")
