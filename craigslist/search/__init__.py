from urllib.parse import urlencode
from craigslist.utils import cdn_url_to_http
from craigslist.data import get_areas

def get_url_base(area):
    areas = get_areas()
    if area not in areas:
        raise ValueError("unknown area {}".format(area))
    tld = areas[area]['tld']
    return "https://{}.craigslist.{}".format(area, tld)

def get_query_url(area, category, type_, offset=0, sort="date", **kwargs):
    params = {"s": offset, "sort": sort, **kwargs}
    params = {k:v for k,v in params.items() if v is not None}
    url = get_url_base(area) + "/{type}/{category}?{params}".format(
        type=type_, category=category, params=urlencode(params))
    return url

from craigslist.search.jsonsearch import jsonsearch, async_jsonsearch
from craigslist.search.regularsearch import regularsearch, async_regularsearch