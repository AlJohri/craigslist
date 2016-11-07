# craigslist

Python wrapper for craigslist.

## Disclaimer

- This library is not associated with Craigslist.
- Please read the Craigslist [terms of use](https://www.craigslist.org/about/terms.of.use.en).

## Usage

```
from craigslist.regularsearch import get_listings
for listing in get_listings():
	print(listing)
```

```
from craigslist.jsonsearch import get_listings
for listing in get_listings():
	print(listing)
```

## Development

### Setup

```
mkvirtualenv craigslist -p python3 -r requirements.txt -a `pwd`
```
