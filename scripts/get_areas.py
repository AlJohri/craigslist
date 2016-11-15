#!/usr/bin/env python3

import json
import requests
import lxml.html
import tldextract
from craigslist.utils import cdn_url_to_http

def get_areas_mapping():
    """
    download list of areas and convert to mapping of hostname to area
    """
    response = requests.get("http://www.craigslist.org/about/areas.json")
    areas = response.json()
    return {x['hostname']:x for x in areas}

# http://www.craigslist.org/about/reference
def get_another_areas_mapping():
    response = requests.get("http://reference.craigslist.org/Areas")
    pass

def get_tlds_mapping(areas_mapping):
    """
    create mapping of country to tld (top level domain)
    """
    redirected_areas = {
        'kootenays': 'cranbrook',
        'vermont': 'burlington'
    }
    tlds = {}

    response = requests.get("http://www.craigslist.org/about/sites")
    doc = lxml.html.fromstring(response.content)
    for a in doc.cssselect("div.box a"):
        url = cdn_url_to_http(a.get('href'))
        parsed_url = tldextract.extract(url)
        area, tld = parsed_url.subdomain, parsed_url.suffix
        area = redirected_areas.get(area, area)
        country = areas_mapping[area]['country']
        tlds[country] = tld
    return tlds

def merge_mappings(areas_mapping, tlds_mapping):
    """
    add tld to each area
    """
    merged_mapping = areas_mapping.copy()
    for hostname, area in merged_mapping.items():
        country = area['country']
        area['tld'] = tlds_mapping[country]
    return merged_mapping

if __name__ == '__main__':
    areas_mapping = get_areas_mapping()
    tlds_mapping = get_tlds_mapping(areas_mapping)
    merged_mapping = merge_mappings(areas_mapping, tlds_mapping)
    print(json.dumps(areas_mapping, indent=4, sort_keys=True))
