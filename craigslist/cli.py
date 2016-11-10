#!/usr/bin/env python3

import sys
import json
import blessings
import itertools
import argparse
import logging
import textwrap
from os import path
from craigslist import search
from craigslist.data import get_areas, DATA_FOLDER
from craigslist.exceptions import CraigslistException
from craigslist.utils import t

def main():
    global_description = """
    examples:
    craigslist search washingtondc apa --postal 20071 --search_distance 1
    craigslist search newyork aap --postal 10023 --search_distance 1 --hasPic --availabilityMode within_30_days --limit 100
    craigslist search sfbay ccc --postal 94305 --search_distance 1 --limit 10
    craigslist search vancouver sss "shoes" --condition new like_new --hasPic --max_price 20 --limit 10
    craigslist search washingtondc jjj --is_telecommuting --is_internship
    craigslist list areas
    """
    global_description = textwrap.dedent(global_description)
    formatter_class = lambda prog: argparse.RawDescriptionHelpFormatter(prog, max_help_position=32)

    parser = argparse.ArgumentParser(
        prog='craigslist',
        description=global_description,
        formatter_class=formatter_class)
    subparsers = parser.add_subparsers(dest='command')
    subparsers.required = True

    shared_parser = argparse.ArgumentParser(add_help=False)
    shared_parser.add_argument('--verbose', default=False, action='store_true')

    with open(path.join(DATA_FOLDER, 'arguments.json')) as f:
        search_arguments = {x['dest']:x for x in json.load(f)}

    def create_search_parser(parent_subparsers, shared_parsers=[]):

        def cli_search(args):
            filter_out_params = ['verbose', 'command', 'area', 'category']
            params = {k:v for k,v in vars(args).items() if v and k not in filter_out_params}

            # subclass ArgumentParser to make this happen automatically
            # it seems to stop using the `choices` parameter if nargs is defined
            for k,v in params.items():
                if k in search_arguments and\
                    search_arguments[k].get('nargs') == '*' and\
                    search_arguments[k].get('choices') is not None and\
                    isinstance(v, list):

                    mapping = search_arguments[k].get('choices')
                    params[k] = [mapping[x] for x in v]
            posts = itertools.islice(
                search(args.area, args.category, **params), 0, args.limit)
            try:
                for post in posts:
                    print(json.dumps(post._asdict()))
            except CraigslistException as e:
                print(t.red(str(e)))
                sys.exit()

        parser = parent_subparsers.add_parser(
            'search',
            usage='%(prog)s area category [options]',
            description=global_description,
            formatter_class=formatter_class,
            help='search',
            parents=shared_parsers)

        parser.add_argument('area')
        parser.add_argument('category')
        parser.add_argument('query', nargs='?', default=None)

        for dest, argument in search_arguments.items():
            x = {k:v for k,v in argument.items() if v is not None}
            parser.add_argument("--" + dest, **x)

        parser.add_argument('--limit', type=int)
        parser.add_argument('--detail', action="store_true")
        parser.add_argument('--executor_class')
        parser.add_argument('--cachedir', help='Cache directory. Defaults to ~/.craigslist')
        parser.add_argument('--nocache', action="store_false", dest='cache', default=True)
        parser.set_defaults(func=cli_search)

    def create_list_parser(parent_subparsers, shared_parsers=[]):

        def cli_list(args):
            if args.entity == "areas":
                areas = get_areas()
                for hostname, area in areas.items():
                    print(area)
            else:
                raise Exception("don't know how to list {}".format(args.entity))

        parser = parent_subparsers.add_parser(
            'list',
            description=global_description,
            formatter_class=formatter_class,
            help='list',
            parents=shared_parsers)

        parser.add_argument('entity', metavar='entity', choices=['areas'])
        parser.set_defaults(func=cli_list)

    create_search_parser(subparsers, shared_parsers=[shared_parser])
    create_list_parser(subparsers, shared_parsers=[shared_parser])

    args = parser.parse_args()

    if args.verbose:
        logging.basicConfig(level=logging.DEBUG, format=
            "[%(name)s | Thread: %(thread)d %(threadName)s | "
            "Process: %(process)d %(processName)s] %(asctime)s %(message)s")
        logging.getLogger('requests').setLevel(logging.WARNING)
        logging.getLogger('urllib3').setLevel(logging.WARNING)
        logging.info('querying with parameters: {}'.format(params))

    args.func(args)

if __name__ == '__main__':
    main()
