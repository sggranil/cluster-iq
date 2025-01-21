import csv
from io import TextIOWrapper


def serialize_datasets(csv_file):
    """
    Serialize the contents of a CSV file and return them as an array of objects.

    Args:
        csv_file (File): The uploaded CSV file to serialize.

    Returns:
        list: A list of dictionaries representing the rows of the CSV file.
    """
    serialized_data = []

    # Open the file and read its contents
    csv_data = TextIOWrapper(csv_file.file, encoding='utf-8')
    reader = csv.DictReader(csv_data)

    for row in reader:
        serialized_data.append(dict(row))

    return serialized_data
