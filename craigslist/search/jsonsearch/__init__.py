import json
import logging
from datetime import datetime, timezone
from craigslist.models import JSONSearchCluster, JSONSearchPost
from craigslist.utils import cdn_url_to_http

logger = logging.getLogger(__name__)

def parse_cluster_url_output(body):
    try:
        items, meta = json.loads(body)
    except ValueError as e:
        logger.error(
            "could not find items and meta "
            "in json response body: '{}'".format(body))
        raise
    try:
        baseurl = cdn_url_to_http(meta['baseurl'])
    except KeyError as e:
        logger.error(
            "could not find baseurl in meta: '{}' "
            "with body:'{}'. probably empty response. "
            "is your query too specific?".format(meta, body))
        raise
    posts = [parse_post(x)
        for x in items if not x.get('GeoCluster')]
    clusters = [parse_cluster(x, baseurl)
        for x in items if x.get('GeoCluster')]
    return posts, clusters

def parse_cluster(cluster, baseurl):
    return JSONSearchCluster(**{
        'id': cluster['GeoCluster'],
        'url': baseurl + cluster['url'],
        'longitude': cluster['Longitude'],
        'latitude': cluster['Latitude'],
        'num_posts': cluster['NumPosts'],
        'posting_ids': cluster['PostingID'].split(','),
        'date': datetime.fromtimestamp(
            float(cluster['PostedDate']), timezone.utc).isoformat()
    })

def parse_post(post):
    return JSONSearchPost(**{
        'id': post['PostingID'],
        'title': post['PostingTitle'],
        'url': cdn_url_to_http(post['PostingURL']),
        'category_id': post['CategoryID'],
        'thumbnail': post.get('ImageThumb'),
        'longitude': post['Longitude'],
        'latitude': post['Latitude'],
        'date': datetime.fromtimestamp(
            float(post['PostedDate']), timezone.utc).isoformat(),
        'price': post['Ask'],
        'bedrooms': post.get('Bedrooms'),
    })

from craigslist.search.jsonsearch.sync import jsonsearch
from craigslist.search.jsonsearch.async import jsonsearch as async_jsonsearch
