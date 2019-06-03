import time
import pytest
import craigslist
import arrow
from itertools import islice
from craigslist.utils import aislice

def sleep(seconds=5):
    print(f'sleeping {seconds} seconds...', end='')
    time.sleep(seconds)
    print('done!')

post_id = None
post_url = None

def test_search_apa():

    sort = lambda x: sorted(x, key=lambda y: y.id)

    sleep()

    gen = craigslist.search('washingtondc', 'apa', postal=20071, search_distance=1, type_='regularsearch')
    posts = sort([post for post in gen])

    sleep()

    gen2 = craigslist.search('washingtondc', 'apa', postal=20071, search_distance=1, type_='jsonsearch')
    posts2 = sort([post for post in gen2])

    A = {x.id for x in posts}
    B = {x.id for x in posts2}

    # instead of assert A == B, lets give it a tolerance of 5
    assert len(A - B) <= 5
    assert len(B - A) <= 5

    # save post id and url for use in a later test
    post = posts[0]
    global post_id, post_url
    post_id = post.id
    post_url = post.url

@pytest.mark.asyncio(forbid_global_loop=False)
async def test_search_apa_async():

    sleep()

    gen = craigslist.search_async('washingtondc', 'apa', postal=20071, search_distance=1)
    posts = [post async for post in gen]

    sleep()

    gen2 = craigslist.search('washingtondc', 'apa', postal=20071, search_distance=1)
    posts2 = [post for post in gen2]

    sort = lambda x: sorted(x, key=lambda y: y.id)
    assert sort(posts) == sort(posts2)

def test_search_apa_with_detail():
    gen = craigslist.search('washingtondc', 'apa', postal=20071, search_distance=1, get_detailed_posts=True)
    post = next(gen)

@pytest.mark.asyncio(forbid_global_loop=False)
async def test_search_apa_with_detail_async():

    sleep()

    gen = craigslist.search_async('washingtondc', 'apa', postal=20071, search_distance=0.1, get_detailed_posts=True)
    posts = [post async for post in gen]

    sleep()

    gen2 = craigslist.search('washingtondc', 'apa', postal=20071, search_distance=0.1, get_detailed_posts=True)
    posts2 = [post for post in gen2]

    sort = lambda x: sorted(x, key=lambda y: y.id)
    assert sort(posts) == sort(posts2)

def test_search_apa_with_clusters_or_pages():

    sleep()

    gen = craigslist.search('washingtondc', 'apa', postal=20071, search_distance=1, type_='regularsearch')
    for post in islice(gen, 0, 200): # force getting at one more page
        pass

    sleep()

    gen2 = craigslist.search('washingtondc', 'apa', postal=20071, search_distance=1)
    for post in islice(gen2, 0, 200): # force getting at least one cluster
        pass

@pytest.mark.asyncio(forbid_global_loop=False)
async def test_search_apa_with_clusters_async():
    sleep()
    gen = craigslist.search_async('washingtondc', 'apa', postal=20071, search_distance=1)
    async for post in aislice(gen, 0, 200): # force getting at least one cluster
        pass

# def test_search_with_debug_executor():
#     sleep()
#     gen = craigslist.search('washingtondc', 'apa', postal=20071, search_distance=1, executor_class='craigslist.io.DebugExecutor')
#     for post in islice(gen, 0, 200): # force getting at least one cluster
#         pass

def test_search_sss():
    sleep()
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

def test_get_fail_post():
    sleep()
    with pytest.raises(craigslist.exceptions.CraigslistException) as e_info:
        post = craigslist.get('https://washingtondc.craigslist.org/nva/apa/5875729002.html')

@pytest.mark.asyncio(forbid_global_loop=False)
async def test_get_post_async():
    sleep()
    id_, url = post_id, post_url # globals
    post = await craigslist.get_async(url)
    assert post.id == id_
    assert post.url == url

@pytest.mark.asyncio(forbid_global_loop=False)
async def test_fail_get_post_async():
    sleep()
    with pytest.raises(craigslist.exceptions.CraigslistException) as e_info:
        post = await craigslist.get_async('https://washingtondc.craigslist.org/nva/apa/5875729002.html')
