#!/usr/bin/env python3

import json
from craigslist.search import query_jsonsearch

if __name__ == '__main__':

	import argparse

	availability_choices = {'all_dates': 0, 'within_30_days': 1, 'beyond_30_days': 2}

	parser = argparse.ArgumentParser(description='Process some integers.')
	parser.add_argument('city')
	parser.add_argument('--postal', help="postal code to center search results around")
	parser.add_argument('--distance', type=int, help="distance in miles from the postal code")
	parser.add_argument('--min_price')
	parser.add_argument('--max_price')
	parser.add_argument('--has_picture', action='store_true', default=None)
	parser.add_argument('--availability', choices=availability_choices)

	args = parser.parse_args()

	params = {
		"postal": args.postal,
		"search_distance": args.distance,
		"min_price": args.min_price,
		"max_price": args.max_price,
		"hasPic": int(args.has_picture) if args.has_picture else None,
		"availabilityMode": availability_choices.get(args.availability)
	}

	posts = [post for post in query_jsonsearch(args.city, **params)]
	print(json.dumps(posts, indent=4, sort_keys=True))
