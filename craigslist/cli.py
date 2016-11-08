#!/usr/bin/env python3

import json
import argparse
import logging
from craigslist import search

class ActionNoYes(argparse.Action):
    def __init__(self, opt_name, dest, default=True, required=False, help=None):
        super(ActionNoYes, self).__init__(['--' + opt_name, '--no-' + opt_name], dest, nargs=0, const=None, default=default, required=required, help=help)
    def __call__(self, parser, namespace, values, option_string=None):
        if option_string.starts_with('--no-'):
            setattr(namespace, self.dest, False)
        else:
            setattr(namespace, self.dest, True)

def main():
    description = """
    examples:
    craigslist search washingtondc --postal 20071 --distance 1 --has_picture --availability within_30_days
    """

    availability_choices = {'all_dates': 0, 'within_30_days': 1, 'beyond_30_days': 2}

    parser = argparse.ArgumentParser(description='Craigslist CLI.')
    parser.add_argument('city')
    parser.add_argument('--postal', help="postal code to center search results around")
    parser.add_argument('--distance', type=int, help="distance in miles from the postal code")
    parser.add_argument('--min_price')
    parser.add_argument('--max_price')
    parser.add_argument('--has_picture', action='store_true', default=None)
    parser.add_argument('--availability', choices=availability_choices)
    parser.add_argument('--verbose', action="store_true")
    parser.add_argument('--detail', action="store_true")
    parser.add_argument('--executor_class')
    parser._add_action(ActionNoYes('cache', 'cache', help="Do (or do not) cache. (default do)"))
    parser.add_argument('--cachedir', help='Cache directory. Defaults to ~/.craigslist')

    args = parser.parse_args()

    if args.verbose:
        logging.basicConfig(level=logging.DEBUG, format=
            "[%(name)s | Thread: %(thread)d %(threadName)s | "
            "Process: %(process)d %(processName)s] %(asctime)s %(message)s")
        logging.getLogger('requests').setLevel(logging.WARNING)
        logging.getLogger('urllib3').setLevel(logging.WARNING)

    params = {
        "get_detailed_posts": args.detail,
        "postal": args.postal,
        "search_distance": args.distance,
        "min_price": args.min_price,
        "max_price": args.max_price,
        "hasPic": int(args.has_picture) if args.has_picture else None,
        "availabilityMode": availability_choices.get(args.availability)
    }

    if args.executor_class:
        params['executor_class'] = args.executor_class

    for post in search(args.city, "apa", **params):
        print(json.dumps(post._asdict()))

if __name__ == '__main__':
    main()
