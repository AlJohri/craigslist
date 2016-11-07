import arrow
import requests
import lxml.html
from urllib.parse import urlencode
from craigslist.utils import cdn_url_to_http

def get_url_base(city):
    return "https://{}.craigslist.org".format(city)

def get_query_url(city, search_type, offset=0, sort="date", **kwargs):
    params = {"s": offset, "sort": sort, **kwargs}
    params = {k:v for k,v in params.items() if v is not None}
    url = get_url_base(city) + "/{}/apa?{}".format(search_type, urlencode(params))
    return url

from craigslist.search.jsonsearch import query_jsonsearch
from craigslist.search.regularsearch import query_regularsearch