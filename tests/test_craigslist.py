import vcr
import pytest
import craigslist

@pytest.mark.asyncio
async def test_search_apa_async():
    gen = await craigslist.search_async('washingtondc', 'apa', postal=20071, search_distance=1)
    posts = [post async for post in gen]

    gen2 = craigslist.search('washingtondc', 'apa', postal=20071, search_distance=1)
    posts2 = [post for post in gen2]

    sort = lambda x: sorted(x, key=lambda y: y.id)

    assert sort(posts) == sort(posts2)

@vcr.use_cassette()
def test_search_apa():
    gen = craigslist.search('washingtondc', 'apa', postal=20071, search_distance=1)
    post = next(gen)

# no vcr (can't use it)
# figure out some way to make this more testable?
def test_search_apa_with_detail():
    gen = craigslist.search('washingtondc', 'apa', postal=20071, search_distance=1, get_detailed_posts=True)
    post = next(gen)

# no vcr (can't use it)
# figure out some way to make this more testable?
def test_search_apa_with_clusters():
    from itertools import islice
    gen = craigslist.search('washingtondc', 'apa', postal=20071, search_distance=1)
    for post in islice(gen, 0, 110): # force getting at least one cluster
        pass

def test_search_with_debug_executor():
    from itertools import islice
    gen = craigslist.search('washingtondc', 'apa', postal=20071, search_distance=1, executor_class='craigslist.io.DebugExecutor')
    for post in islice(gen, 0, 110): # force getting at least one cluster
        pass

@vcr.use_cassette()
def test_search_sss():
    gen = craigslist.search('vancouver', 'sss', query='shoes', condition=[10,20], hasPic=1, max_price=20)
    post = next(gen)

def test_get_url_base():
    from craigslist._search import get_url_base
    assert get_url_base('washingtondc') == 'https://washingtondc.craigslist.org'
    assert get_url_base('aberdeen') == 'https://aberdeen.craigslist.co.uk'
    with pytest.raises(ValueError) as e_info:
        get_url_base('asdadf')

def test_get_query_url():
    from craigslist._search import get_query_url
    assert "https://washingtondc.craigslist.org/jsonsearch/apa" in get_query_url('washingtondc', 'apa', 'jsonsearch')
    with pytest.raises(ValueError) as e_info:
        get_query_url('washingtondc', 'errorerrorerror', 'jsonsearch')

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

@vcr.use_cassette()
def test_get_post():
    url = 'https://washingtondc.craigslist.org/nva/apa/6129297133.html'
    post = craigslist.get(url)
    assert post.id == 6129297133
    assert post.url == url
