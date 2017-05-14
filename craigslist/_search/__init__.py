import os
import functools
from urllib.parse import urlencode
from craigslist.utils import cdn_url_to_http, import_class
from craigslist.data import get_areas, get_categories
from craigslist.io import requests_get, asyncio_get
from craigslist.post import get_posts, get_posts_async
from craigslist.exceptions import (
    CraigslistException, CraigslistValueError)

@functools.lru_cache(maxsize=None)
def get_url_base(area):
    areas = get_areas()
    if area not in areas:
        raise CraigslistValueError("unknown area {}".format(area))
    tld = areas[area]['tld']
    return "https://{}.craigslist.{}".format(area, tld)

def get_query_url(area, category, type_, offset=0, sort="date", **kwargs):
    categories = get_categories()
    if category not in categories:
        raise CraigslistValueError("unknown category {}".format(category))
    params = {"s": offset, "sort": sort, **kwargs}
    params_expanded = []
    for k,v in params.items():
        if v is None: continue
        if isinstance(v, list):
            for x in v:
                params_expanded.append((k, x))
        else:
            params_expanded.append((k,v))
    url = get_url_base(area) + "/{type}/{category}?{params}".format(
        type=type_, category=category, params=urlencode(params_expanded))
    return url

def make_executor(executor_class, max_workers=None):
    if isinstance(executor_class, str):
        executor_class = import_class(executor_class)
    return executor_class(max_workers=max_workers)

from craigslist._search.jsonsearch import jsonsearch
from craigslist._search.regularsearch import regularsearch

def search(
    area,
    category,
    type_="jsonsearch",
    get_detailed_posts=False,
    cache=True,
    cachedir=os.path.expanduser('~'),
    executor=None,
    executor_class='concurrent.futures.ThreadPoolExecutor',
    max_workers=None,
    get=requests_get,
    **kwargs):

    def extract_post_urls(posts):
        yield from (post.url for post in posts)

    executor = executor or make_executor(executor_class, max_workers)

    search_funcs = {
        "jsonsearch": jsonsearch,
        "regularsearch": regularsearch}

    try:
        search_func = search_funcs[type_]
    except IndexError: # pragma: no cover
        raise CraigslistValueError("unknown search type: {}".format(type_))

    search_gen = search_func(
        area, category, type_, cache, cachedir, executor, get, **kwargs)

    if get_detailed_posts:
        ret_gen = get_posts(extract_post_urls(search_gen), executor, get)
    else:
        ret_gen = search_gen

    return ret_gen

from craigslist._search.jsonsearch import jsonsearch_async

async def search_async(
    area,
    category,
    type_="jsonsearch",
    get_detailed_posts=False,
    cache=True,
    cachedir=os.path.expanduser('~'),
    max_workers=None,
    get=asyncio_get,
    **kwargs):

    async def extract_post_urls(posts):
        async for post in posts:
            yield post.url

    search_funcs = {"jsonsearch": jsonsearch_async}

    try:
        search_func = search_funcs[type_]
    except IndexError: # pragma: no cover
        raise CraigslistValueError("unknown search type: {}".format(type_))

    search_gen = search_func(
        area, category, type_, cache, cachedir, get, **kwargs)

    if get_detailed_posts:
        ret_gen = get_posts_async(extract_post_urls(search_gen), get)
    else:
        ret_gen = search_gen

    async for post in ret_gen:
        yield post
