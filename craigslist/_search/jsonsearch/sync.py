import logging
from concurrent.futures import as_completed
from craigslist._search import get_query_url
from craigslist._search.jsonsearch import process_cluster_url
from craigslist.post import process_post_url

logger = logging.getLogger(__name__)

# http://stackoverflow.com/questions/1747963/multiprocessing-pool-inside-process-time-out/1748335#1748335
# You can't pass Pool objects between processes.

def jsonsearch(
    area,
    category,
    sort,
    cache,
    cachedir,
    executor,
    get,
    **kwargs):

    def process_clusters(clusters, executor):
        futures = [executor.submit(
            process_cluster_url, cluster.url, get) for cluster in clusters]
        for future in as_completed(futures):
            posts, clusters = future.result()
            yield from posts
            process_clusters(clusters, executor)

    url = get_query_url(area, category, "jsonsearch", sort=sort, **kwargs)
    posts, clusters = process_cluster_url(url, get)
    yield from posts
    yield from process_clusters(clusters, executor)
