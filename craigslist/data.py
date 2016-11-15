import json
import functools
from os import path
DATA_FOLDER = path.join(path.dirname(path.realpath(__file__)), "data")

@functools.lru_cache(maxsize=None)
def get_areas():
    with open(path.join(DATA_FOLDER, 'areas.json')) as f:
        return json.load(f)

@functools.lru_cache(maxsize=None)
def get_categories():
    with open(path.join(DATA_FOLDER, 'categories.json')) as f:
        return json.load(f)
