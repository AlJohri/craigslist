import logging
from concurrent.futures import as_completed
from craigslist.search import get_query_url
from craigslist.utils import import_class
from craigslist.post import process_post_url
from craigslist.io import get
from craigslist.search.jsonsearch import parse_cluster_url_output

logger = logging.getLogger(__name__)

def jsonsearch(
    area,
    category,
    sort="date",
    get_detailed_posts=False,
    get=get,
    executor_class='concurrent.futures.ThreadPoolExecutor',
    max_workers=None,
    **kwargs):

    if isinstance(executor_class, str):
        executor_class = import_class(executor_class)
    post_executor = executor_class(max_workers=max_workers)
    cluster_executor = executor_class(max_workers=max_workers)

    def process_posts(posts, post_executor):
        futures = [post_executor.submit(
            process_post_url, post.url, get) for post in posts]
        for future in as_completed(futures):
            post = future.result()
            yield post

    def process_clusters(clusters, cluster_executor):
        futures = [cluster_executor.submit(
            process_cluster_url, cluster.url, get) for cluster in clusters]
        for future in as_completed(futures):
            posts, clusters = future.result()
            if get_detailed_posts:
                yield from process_posts(posts, post_executor)
            else:
                yield from posts
            process_clusters(clusters, cluster_executor)

    url = get_query_url(area, category, "jsonsearch", sort=sort, **kwargs)
    posts, clusters = process_cluster_url(url, get)
    if get_detailed_posts:
        yield from process_posts(posts, post_executor)
    else:
        yield from posts
    yield from process_clusters(clusters, cluster_executor)

def process_cluster_url(url, get):
    logger.debug("downloading %s" % url)
    body = get(url)
    return parse_cluster_url_output(body)
