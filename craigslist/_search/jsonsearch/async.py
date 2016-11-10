import logging
from craigslist._search.jsonsearch import parse_cluster_url_output
from craigslist.io import asyncio_get, asyncio_queue

logger = logging.getLogger(__name__)

# http://www.tornadoweb.org/en/stable/guide/coroutines.html#python-3-5-async-and-await
# http://www.tornadoweb.org/en/stable/guide/queues.html

# https://docs.python.org/3/library/asyncio.html

# need a parameter for a function that given a coroutine it will schedule that coroutine
# to occur. this way I don't need an explicit event loop to be passed in

# see if this can be done without an explicit queue?

async def jsonsearch(
    area,
    category,
    sort,
    get_detailed_posts,
    cache,
    cachedir,
    get=asyncio_get,
    queue_class=asyncio_queue,
    **kwargs):

    page_queue = queue_class(maxsize=CONCURRENCY)
    post_queue = queue_class(maxsize=CONCURRENCY)

    async def page_worker():
        while True:
            current_job = await page_queue.get()

    async def post_worker():
        while True:
            current_job = await post_queue.get()

    # for i in range(max_workers):
        # asyncio.
        # ioloop.IOLoop.current().spawn_callback(worker, i)

async def process_cluster_url(url, get):
    logger.debug("downloading %s" % url)
    body = await get(url)
    return parse_cluster_url_output(body)