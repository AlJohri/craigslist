import os
from urllib.parse import urlencode
from craigslist.utils import cdn_url_to_http, import_class
from craigslist.data import get_areas
from craigslist.io import requests_get
from craigslist.post import get_posts

def get_url_base(area):
    areas = get_areas()
    if area not in areas:
        raise ValueError("unknown area {}".format(area))
    tld = areas[area]['tld']
    return "https://{}.craigslist.{}".format(area, tld)

def get_query_url(area, category, type_, offset=0, sort="date", **kwargs):
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

from craigslist._search.jsonsearch import jsonsearch #, async_jsonsearch
from craigslist._search.regularsearch import regularsearch #, async_regularsearch

def make_executor(executor_class, max_workers=None):
    if isinstance(executor_class, str):
        executor_class = import_class(executor_class)
    return executor_class(max_workers=max_workers)

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

    if type_ == "jsonsearch":
        search_gen = jsonsearch(
            area, category, type_, cache, cachedir, executor, get, **kwargs)
    elif type_ == "regularsearch":
        search_gen = regularsearch(
            area, category, type_, cache, cachedir, executor, get, **kwargs)
    else:
        raise Exception("unknown search type")

    if get_detailed_posts:
        ret_gen = get_posts(extract_post_urls(search_gen), executor, get)
    else:
        ret_gen = search_gen

    return ret_gen
