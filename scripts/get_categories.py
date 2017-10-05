#!/usr/bin/env python3

import re, requests, json
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

# https://newyork.craigslist.org/i/apartments
# https://sfbay.craigslist.org/i/autos
# https://portland.craigslist.org/i/computers
missing_categories = {
    'aap': {
        'abbreviation': 'aap',
        'category_id': None,
        'description': 'all apartments',
        'type': 'H'
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
}

def get_categories_mapping():
    response = requests.get("http://reference.craigslist.org/Categories")
    categories = [convert_dict_to_camel_case(x) for x in response.json()]
    categories_mapping = {x['abbreviation']:x for x in categories}
    categories_mapping.update(missing_categories)
    categories_mapping.update(top_level_categories)
    return categories_mapping

if __name__ == '__main__':
    categories_mapping = get_categories_mapping()
    print(json.dumps(categories_mapping, indent=4, sort_keys=True))