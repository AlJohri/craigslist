import json
import logging
from collections import namedtuple
from datetime import datetime, timezone
from craigslist.utils import cdn_url_to_http
from craigslist.exceptions import CraigslistException

logger = logging.getLogger(__name__)

JSONSearchPost = namedtuple('JSONSearchPost', [
    'id',
    'title',
    'url',
    'category_id',
    'thumbnail',
    'longitude',
    'latitude',
    'date',
    'price',
    'bedrooms'])

JSONSearchCluster = namedtuple('JSONSearchCluster', [
    'id',
    'url',
    'longitude',
    'latitude',
    'posting_ids',
    'num_posts',
    'date'])

def parse_cluster_url_output(body):
    try:
        items, meta = json.loads(body)
    except ValueError as e: # pragma: no cover
        raise CraigslistException(
            "could not find items and meta "
            "in json response body: '{}'".format(body))
    try:
        baseurl = cdn_url_to_http(meta['baseurl'])
    except KeyError as e: # pragma: no cover
        raise CraigslistException(
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
        'id': int(cluster['GeoCluster']),
        'url': baseurl + cluster['url'],
        'longitude': cluster['Longitude'],
        'latitude': cluster['Latitude'],
        'num_posts': cluster['NumPosts'],
        'posting_ids': [int(x) for x in cluster['PostingID'].split(',')],
        'date': datetime.fromtimestamp(
            float(cluster['PostedDate']), timezone.utc).isoformat()
    })

def parse_post(post):
    return JSONSearchPost(**{
        'id': int(post['PostingID']),
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

import concurrent.futures
from craigslist._search import get_query_url
from craigslist.post import process_post_url

# http://stackoverflow.com/questions/1747963/multiprocessing-pool-inside-process-time-out/1748335#1748335
# You can't pass Pool objects between processes.

def process_cluster_url(url, get):
    logger.debug("downloading %s" % url)
    body = get(url)
    return parse_cluster_url_output(body)

def jsonsearch(
    area,
    category,
    sort,
    cache,
    cachedir,
    executor,
    get,
    as_completed=concurrent.futures.as_completed,
    **kwargs):

    def process_clusters(clusters, executor):
        futures = (executor.submit(
            process_cluster_url, cluster.url, get) for cluster in clusters)
        try:
            for future in as_completed(futures):
                posts, clusters = future.result()
                yield from posts
                process_clusters(clusters, executor)
        except KeyboardInterrupt:  # pragma: no cover
            for future in futures:
                future.cancel()

    url = get_query_url(area, category, "jsonsearch", sort=sort, **kwargs)
    posts, clusters = process_cluster_url(url, get)
    yield from posts
    yield from process_clusters(clusters, executor)

import asyncio

async def process_cluster_url_async(url, get):
    logger.debug("downloading %s" % url)
    body = await get(url)
    return parse_cluster_url_output(body)

async def jsonsearch_async(
    area,
    category,
    sort,
    cache,
    cachedir,
    get,
    as_completed=asyncio.as_completed,
    **kwargs):

    async def process_clusters(clusters):
        futures = [process_cluster_url(cluster.url) for cluster in clusters]
        try:
            for future in as_completed(futures):
                posts, clusters = await future
                for post in posts:
                    yield post
                async for post in process_clusters(clusters):
                    yield post
        except KeyboardInterrupt: # pragma: no cover
            for future in futures:
                future.cancel()

    url = get_query_url(area, category, "jsonsearch", sort=sort, **kwargs)
    posts, clusters = await process_cluster_url_async(url, get)
    for post in posts:
        yield post
    async for post in process_clusters(clusters):
        yield post
