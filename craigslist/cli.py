#!/usr/bin/env python3

import json
import argparse
import logging
import textwrap
from os import path
from craigslist import search
from craigslist.data import DATA_FOLDER

def main():
    description = """
    examples:
    craigslist search washingtondc apa --postal 20071 --search_distance 1 --hasPic --availabilityMode within_30_days
    """

    parser = argparse.ArgumentParser(
        prog='craigslist',
        description=textwrap.dedent(description),
        formatter_class=argparse.RawTextHelpFormatter    )
    subparsers = parser.add_subparsers(dest='command')
    subparsers.required = True

    def create_search_parser(parent_subparsers):
        parser = parent_subparsers.add_parser(
            'search',
            usage='%(prog)s area category [options]',
            help='get resources')
        parser.add_argument('area')
        parser.add_argument('category')

        with open(path.join(DATA_FOLDER, 'arguments.json')) as f:
            arguments = json.load(f)

        for argument in arguments:
            x = {k:v for k,v in argument.items() if v is not None}
            parser.add_argument("--" + argument['dest'], **x)

        parser.add_argument('--verbose', action="store_true")
        parser.add_argument('--detail', action="store_true")
        parser.add_argument('--executor_class')
        parser.add_argument('--cachedir', help='Cache directory. Defaults to ~/.craigslist')
        parser.add_argument('--nocache', action="store_false", dest='cache', default=True)

    create_search_parser(subparsers)

    args = parser.parse_args()

    if args.verbose:
        logging.basicConfig(level=logging.DEBUG, format=
            "[%(name)s | Thread: %(thread)d %(threadName)s | "
            "Process: %(process)d %(processName)s] %(asctime)s %(message)s")
        logging.getLogger('requests').setLevel(logging.WARNING)
        logging.getLogger('urllib3').setLevel(logging.WARNING)

    filter_out_params = ['verbose', 'command', 'area', 'category']
    params = {k:v for k,v in vars(args).items() if v and k not in filter_out_params}

    for post in search(args.area, args.category, **params):
        print(json.dumps(post._asdict()))

if __name__ == '__main__':
    main()
