import vcr
from craigslist import search

@vcr.use_cassette()
def test_search_apa():
    gen = search('washingtondc', 'apa', postal=20071, search_distance=1)
    post = next(gen)

@vcr.use_cassette()
def test_search_sss():
    gen = search('vancouver', 'sss', query='shoes', condition=[10,20], hasPic=1, max_price=20)
    post = next(gen)
