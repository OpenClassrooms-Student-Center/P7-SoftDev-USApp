import json
from pathlib import Path

DATA_FOLDER = "data"


def _json_from_file(filename, key):
    filepath = Path(__file__).parent / DATA_FOLDER / filename
    with open(filepath) as fp:
        data = json.load(fp)
        return data[key]


def get_clubs():
    return _json_from_file("clubs.json", "clubs")


def get_competitions():
    return _json_from_file("competitions.json", "competitions")
