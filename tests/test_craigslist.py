import vcr
from craigslist import search

@vcr.use_cassette()
def test_search_sync():
    gen = search('washingtondc', 'apa', postal=20071, search_distance=1)
    post = next(gen)