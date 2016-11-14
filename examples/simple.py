#!/usr/bin/env python3

import craigslist

def main()
    for post in craigslist.search('washingtondc', 'apa', postal=20071, search_distance=1):
        print(post)

if __name__ == '__main__':
    main()
