import json, arrow, queue, logging
from craigslist.models import JSONSearchPost
from craigslist.search import get_query_url
from craigslist.utils import cdn_url_to_http
from craigslist.io import (
    ThreadPoolExecutor, ProcessPoolExecutor, FakeExecutor, 
    as_completed, get, async_get)

logging.basicConfig(level=logging.DEBUG, format='[%(name)s | Thread: %(thread)d %(threadName)s | Process: %(process)d %(processName)s] %(asctime)s %(message)s')
logging.getLogger('requests').setLevel(logging.WARNING)
logging.getLogger('urllib3').setLevel(logging.WARNING)
logger = logging.getLogger(__name__)

def query_jsonsearch(city, sort="date", get=get, get_detailed_posts=False, executor_class=ThreadPoolExecutor, max_workers=None, **kwargs):
    post_executor = executor_class(max_workers=max_workers)
    cluster_executor = executor_class(max_workers=max_workers)

    def process_posts(posts, post_executor):
        futures = [post_executor.submit(
            process_post_url, post['url']) for post in posts]
        for future in as_completed(futures):
            post = future.result()
            yield post

    def process_clusters(clusters, cluster_executor):
        futures = [cluster_executor.submit(
            process_cluster_url, cluster['url']) for cluster in clusters]
        for future in as_completed(futures):
            posts, clusters = future.result()
            if get_detailed_posts:
                yield from process_posts(posts, post_executor)
            else:
                yield from posts
            process_clusters(clusters, cluster_executor)
    
    url = get_query_url(city, "jsonsearch", sort=sort, **kwargs)
    posts, clusters = process_cluster_url(url)
    if get_detailed_posts:
        yield from process_posts(posts, post_executor)
    else:
        yield from posts
    yield from process_clusters(clusters, cluster_executor)

def process_post_url(url):
    logger.debug("downloading %s" % url)
    body = get(url)
    post = body # parse stuff
    return post

def process_cluster_url(url):
    logger.debug("downloading %s" % url)
    body = get(url)
    items, meta = json.loads(body)
    baseurl = cdn_url_to_http(meta['baseurl'])
    posts = [process_post_json(x) for x in items if not x.get('GeoCluster')]
    clusters = [x for x in items if x.get('GeoCluster')]
    for cluster in clusters:
        cluster['url'] = baseurl + cluster['url']
    return posts, clusters

def process_post_json(post):
    return JSONSearchPost(**{
        'id': post['PostingID'],
        'title': post['PostingTitle'],
        'url': cdn_url_to_http(post['PostingURL']),
        'longitude': post['Longitude'],
        'latitude': post['Latitude'],
        'price': post['Ask'],
        'bedrooms': post['Bedrooms'],
        'date': arrow.get(post['PostedDate']).isoformat(),
        'thumbnail': post.get('ImageThumb'),
        'category_id': post['CategoryID'],
    })

if __name__ == '__main__':

    for x in query_jsonsearch('washingtondc', executor_class=ThreadPoolExecutor, postal=20071, search_distance=1):
        pass

    # for x in query_jsonsearch('washingtondc', executor_class=ProcessPoolExecutor, postal=20071, search_distance=1):
    #     pass

    # for x in query_jsonsearch('washingtondc', executor_class=FakeExecutor, postal=20071, search_distance=1):
    #     pass
