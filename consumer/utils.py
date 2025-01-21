import csv
import datetime
import pytz

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


def parse_timestamp(date_string):
    try:
        date_string = date_string.replace("GMT", "").strip()

        if date_string[-1].isdigit() and date_string[-2] in "+-":
            date_string = date_string[:-1] + "0" + date_string[-1] + ":00"

        date_format = "%Y/%m/%d %I:%M:%S %p %z"
        parsed_date = datetime.datetime.strptime(date_string, date_format)

        timezone = pytz.timezone("Asia/Singapore")
        timezone_aware_date = parsed_date.astimezone(timezone)

        return timezone_aware_date
    except ValueError:
        raise ValueError(f"Timestamp '{date_string}' has an invalid format.")
