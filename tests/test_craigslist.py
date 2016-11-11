import vcr
import pytest
from craigslist import search

@vcr.use_cassette()
def test_search_apa():
    gen = search('washingtondc', 'apa', postal=20071, search_distance=1)
    post = next(gen)

# no vcr (can't use it)
# figure out some way to make this more testable?
def test_search_apa_with_detail():
    gen = search('washingtondc', 'apa', postal=20071, search_distance=1, get_detailed_posts=True)
    post = next(gen)

# no vcr (can't use it)
# figure out some way to make this more testable?
def test_search_apa_with_clusters():
    from itertools import islice
    gen = search('washingtondc', 'apa', postal=20071, search_distance=1)
    for post in islice(gen, 0, 110): # force getting at least one cluster
        pass

@vcr.use_cassette()
def test_search_sss():
    gen = search('vancouver', 'sss', query='shoes', condition=[10,20], hasPic=1, max_price=20)
    post = next(gen)

def test_get_url_base():
    from craigslist._search import get_url_base
    assert get_url_base('washingtondc') == 'https://washingtondc.craigslist.org'
    assert get_url_base('aberdeen') == 'https://aberdeen.craigslist.co.uk'
    with pytest.raises(ValueError) as e_info:
        get_url_base('asdadf')

def test_import_class():
    from craigslist.utils import import_class
    from concurrent.futures import ThreadPoolExecutor
    assert import_class('concurrent.futures.ThreadPoolExecutor') == ThreadPoolExecutor
    with pytest.raises(ValueError) as e_info:
        import_class('JustAClassNameWithNoPath')
    with pytest.raises(ImportError) as e_info:
        import_class('mypath.that.doesntexist.ImaginaryClass')

def test_cli():
    from craigslist.cli import cli
    with pytest.raises(SystemExit) as e_info:
        args = cli()
