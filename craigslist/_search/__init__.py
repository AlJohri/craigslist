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

from craigslist._search.jsonsearch import jsonsearch, async_jsonsearch
from craigslist._search.regularsearch import regularsearch, async_regularsearch