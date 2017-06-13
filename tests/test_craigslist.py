import vcr
import pytest
import craigslist
import arrow
from itertools import islice
from craigslist.utils import aislice

post_id = None
post_url = None

def test_search_apa():
    gen = craigslist.search('washingtondc', 'apa', postal=20071, search_distance=1, type_='regularsearch')
    post = next(gen)

    gen2 = craigslist.search('washingtondc', 'apa', postal=20071, search_distance=1)
    post2 = next(gen2)

    assert post.id == post2.id
    assert post.title == post2.title
    assert arrow.get(post.date) == arrow.get(post2.date).replace(second=0)

    # save post id and url for use in a later test
    global post_id, post_url
    post_id = post.id
    post_url = post.url

@pytest.mark.asyncio(forbid_global_loop=False)
async def test_search_apa_async():
    gen = craigslist.search_async('washingtondc', 'apa', postal=20071, search_distance=1)
    posts = [post async for post in gen]

    gen2 = craigslist.search('washingtondc', 'apa', postal=20071, search_distance=1)
    posts2 = [post for post in gen2]

    sort = lambda x: sorted(x, key=lambda y: y.id)
    assert sort(posts) == sort(posts2)

def test_search_apa_with_detail():
    gen = craigslist.search('washingtondc', 'apa', postal=20071, search_distance=1, get_detailed_posts=True)
    post = next(gen)

@pytest.mark.asyncio(forbid_global_loop=False)
async def test_search_apa_with_detail_async():
    gen = craigslist.search_async('washingtondc', 'apa', postal=20071, search_distance=0.1, get_detailed_posts=True)
    posts = [post async for post in gen]

    gen2 = craigslist.search('washingtondc', 'apa', postal=20071, search_distance=0.1, get_detailed_posts=True)
    posts2 = [post for post in gen2]

    sort = lambda x: sorted(x, key=lambda y: y.id)
    assert sort(posts) == sort(posts2)

def test_search_apa_with_clusters_or_pages():
    gen = craigslist.search('washingtondc', 'apa', postal=20071, search_distance=1, type_='regularsearch')
    for post in islice(gen, 0, 110): # force getting at one more page
        pass

    gen2 = craigslist.search('washingtondc', 'apa', postal=20071, search_distance=1)
    for post in islice(gen2, 0, 110): # force getting at least one cluster
        pass

@pytest.mark.asyncio(forbid_global_loop=False)
async def test_search_apa_with_clusters_async():
    gen = craigslist.search_async('washingtondc', 'apa', postal=20071, search_distance=1)
    async for post in aislice(gen, 0, 110): # force getting at least one cluster
        pass

def test_search_with_debug_executor():
    gen = craigslist.search('washingtondc', 'apa', postal=20071, search_distance=1, executor_class='craigslist.io.DebugExecutor')
    for post in islice(gen, 0, 110): # force getting at least one cluster
        pass

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

def test_get_post():
    id_, url = post_id, post_url # globals
    post = craigslist.get(url)
    assert post.id == post_id
    assert post.url == url

@pytest.mark.asyncio(forbid_global_loop=False)
async def test_get_post_async():
    id_, url = post_id, post_url # globals
    post = await craigslist.get_async(url)
    assert post.id == id_
    assert post.url == url
