#!/usr/bin/env python3

import re
import json
import requests
import lxml.html
from craigslist.utils import convert_dict_to_camel_case

top_level_categories = {
    'ccc': {
        'abbreviation': 'ccc',
        'category_id': None,
        'description': 'community',
        'type': 'C'
    },
    'hhh': {
        'abbreviation': 'hhh',
        'category_id': None,
        'description': 'housing',
        'type': 'H'
    },
    'jjj': {
        'abbreviation': 'jjj',
        'category_id': None,
        'description': 'jobs',
        'type': 'J'
    },
    'ggg': {
        'abbreviation': 'ggg',
        'category_id': None,
        'description': 'gigs',
        'type': 'G'
    },
    'rrr': {
        'abbreviation': 'rrr',
        'category_id': None,
        'description': 'resumes',
        'type': 'R'
    },
    'bbb': {
        'abbreviation': 'bbb',
        'category_id': None,
        'description': 'services',
        'type': 'B'
    },
    'sss': {
        'abbreviation': 'sss',
        'category_id': None,
        'description': 'for sale',
        'type': 'S'
    },
    'ppp': {
        'abbreviation': 'ppp',
        'category_id': None,
        'description': 'personals',
        'type': 'P'
    }
}

missing_categories = {
    'aap': {
        'abbreviation': 'aap',
        'category_id': None,
        'description': 'all apartments',
        'type': 'H'
    },
    'nfa': {
        'abbreviation': 'nfa',
        'category_id': None,
        'description': 'no-fee apartments',
        'type': 'H',
    },
    'cta': {
        'abbreviation': 'cta',
        'category_id': None,
        'description': 'cars & trucks',
        'type': 'S'
    },
    'sya': {
        'abbreviation': 'sya',
        'category_id': None,
        'description': 'computers',
        'type': 'S'
    },
    'syp': {
        'abbreviation': 'syp',
        'category_id': None,
        'description': 'computer parts',
        'type': 'S'
    },
    'wta': {
        'abbreviation': 'wta',
        'category_id': None,
        'description': 'auto wheels & tires',
        'type': 'S'
    },
    'pta': {
        'abbreviation': 'pta',
        'category_id': None,
        'description': 'auto parts',
        'type': 'S'
    },
    'bia': {
        'abbreviation': 'bia',
        'category_id': None,
        'description': 'bicycles',
        'type': 'S'
    },
    'bip': {
        'abbreviation': 'bip',
        'category_id': None,
        'description': 'bicycle parts',
        'type': 'S',
    },
    'boo': {
        'abbreviation': 'boo',
        'category_id': None,
        'description': 'boats',
        'type': 'S'
    },
    'bpa': {
        'abbreviation': 'bpa',
        'category_id': None,
        'description': 'boat parts',
        'type': 'S'
    },
    'mca': {
        'abbreviation': 'mca',
        'category_id': None,
        'description': 'motorcycles/scooters',
        'type': 'S'
    },
    'mpa': {
        'abbreviation': 'mpa',
        'category_id': None,
        'description': 'motorcycle parts',
        'type': 'S'
    },
}

def get_categories_mapping():
    response = requests.get("http://reference.craigslist.org/Categories")
    categories = [convert_dict_to_camel_case(x) for x in response.json()]
    categories_mapping = {x['abbreviation']:x for x in categories}
    categories_mapping.update(missing_categories)
    categories_mapping.update(top_level_categories)
    return categories_mapping

def get_missing_categories():
    """
    not fully implemented. hardcoded above as `missing_categories` for now

    common meta categories:

    /i/apartments
    /i/auto_parts
    /i/bikes
    /i/boats
    /i/autos
    /i/computers
    /i/motorcycles
    """
    areas = ['nyc', 'sfbay', 'washingtondc', 'chicago']
    for area in areas:
        response = requests.get(f"http://{area}.craigslist.org")
        doc = lxml.html.fromstring(response.content)
        for x in doc.cssselect("#center a[href*='/i/']"):
            print(x.get('href'))

if __name__ == '__main__':
    categories_mapping = get_categories_mapping()
    print(json.dumps(categories_mapping, indent=4, sort_keys=True))
