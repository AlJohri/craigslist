# craigslist

Python wrapper for craigslist.

*NOTE*: This library is a WIP. The API is not stable.

## Disclaimer

- This library is not associated with Craigslist.
- Please read the Craigslist [terms of use](https://www.craigslist.org/about/terms.of.use.en).

## Install
```
pip3 install --upgrade git+https://github.com/AlJohri/craigslist.git
```

## API

```
from craigslist import search

for post in search('washingtondc', 'apa', postal=20071, search_distance=1):
    print(post)

async for post in search('washingtondc', 'apa', postal=20071, search_distance=1):
    print(post)
```

## CLI

```
usage: craigslist [-h] [--postal POSTAL] [--distance DISTANCE]
                  [--min_price MIN_PRICE] [--max_price MAX_PRICE]
                  [--has_picture]
                  [--availability {all_dates,beyond_30_days,within_30_days}]
                  [--verbose] [--detail] [--executor_class EXECUTOR_CLASS]
                  [--cache] [--cachedir CACHEDIR]
                  city

Craigslist CLI.

positional arguments:
  city

optional arguments:
  -h, --help            show this help message and exit
  --postal POSTAL       postal code to center search results around
  --distance DISTANCE   distance in miles from the postal code
  --min_price MIN_PRICE
  --max_price MAX_PRICE
  --has_picture
  --availability {all_dates,beyond_30_days,within_30_days}
  --verbose
  --detail
  --executor_class EXECUTOR_CLASS
  --cache, --no-cache   Do (or do not) cache. (default do)
  --cachedir CACHEDIR   Cache directory. Defaults to ~/.craigslist
```

## Development

### Setup

```
make virtualenv install
```
