#!/usr/bin/env python3

import sys
import json
import requests
import lxml.html
import tldextract
from craigslist.utils import cdn_url_to_http
from craigslist.utils import convert_dict_to_camel_case

def get_areas_mapping_old():
    """
    download list of areas and convert to mapping of hostname to area
    """
    redirected_hostnames = {
        'cranbrook': 'kootenays',
        'burlington': 'vermont'
    }
    response = requests.get("http://www.craigslist.org/about/areas.json")
    areas = response.json()
    for area in areas:
        hostname = area['hostname']
        area['hostname'] = redirected_hostnames.get(hostname, hostname)
    return {x['hostname']:x for x in areas}

def get_areas_mapping():
    """
    download list of areas and convert to mapping of hostname to area
    """
    response = requests.get("http://reference.craigslist.org/Areas")
    areas = [convert_dict_to_camel_case(x) for x in response.json()]
    areas_mapping = {x['hostname']:x for x in areas}
    return areas_mapping

def get_tlds_mapping(areas_mapping):
    """
    create mapping of country to tld (top level domain)
    """
    tlds = {}

    redirected_hostnames = {
        'fortlauderdale': 'miami'
    }

    response = requests.get("http://www.craigslist.org/about/sites")
    doc = lxml.html.fromstring(response.content)
    for a in doc.cssselect("div.box a"):
        url = cdn_url_to_http(a.get('href'))
        parsed_url = tldextract.extract(url)
        area, tld = parsed_url.subdomain, parsed_url.suffix
        area = redirected_hostnames.get(area, area)
        try:
            country = areas_mapping[area]['country']
        except KeyError:
            print("could not found {} in areas_mapping".format(area), file=sys.stderr)
            continue
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
    print(json.dumps(merged_mapping, indent=4, sort_keys=True))
