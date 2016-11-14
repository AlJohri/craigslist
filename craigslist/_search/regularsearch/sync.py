import logging
from concurrent.futures import as_completed
from craigslist.utils import import_class
from craigslist.io import requests_get
from craigslist._search import get_query_url
# from craigslist._search.regularsearch import process_page_url
from craigslist.post import process_post_url

def regularsearch(area, sort="date", **kwargs):
    doc = lxml.html.fromstring(requests.get(get_query_url(
        area, "search", offset=0, sort=sort, **kwargs)))
    num_total_posts = get_num_total_posts_from_response(doc)
    num_posts_on_page = get_number_of_posts_on_current_page_from_response(doc)
    yield from get_posts_from_response(doc)
    for offset in range(100, num_total_posts, 100):
        doc = lxml.html.fromstring(requests.get(get_query_url(
            area, "search", offset=offset, sort=sort, **kwargs)))
        num_posts_on_page = get_number_of_posts_on_current_page_from_response(doc)
        yield from get_posts_from_response(doc)
