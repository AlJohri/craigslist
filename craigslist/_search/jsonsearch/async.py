import logging
from craigslist._search.jsonsearch import parse_cluster_url_output
from craigslist.io import asyncio_get

logger = logging.getLogger(__name__)

# http://www.tornadoweb.org/en/stable/guide/coroutines.html#python-3-5-async-and-await
# http://www.tornadoweb.org/en/stable/guide/queues.html

# https://docs.python.org/3/library/asyncio.html

async def jsonsearch(
    area,
    category,
    sort,
    get_detailed_posts,
    cache,
    cachedir,
    get=asyncio_get,
    **kwargs):
    
    raise NotImplementedError()

    # q = queues.Queue(maxsize=CONCURRENCY)

    # async def worker():
        # while True:
            # current_job = await q.get()
            # key = "%s-%s-%s" % (current_job.year, current_job.discipline_code, current_job.endpoint)
            # start_time = ioloop.IOLoop.current().time()
            # await single_job(current_job, i)
            # end_time = ioloop.IOLoop.current().time()

    # for i in range(max_workers):
        # asyncio.
        # ioloop.IOLoop.current().spawn_callback(worker, i)

    pass

async def process_cluster_url(url, get):
    logger.debug("downloading %s" % url)
    body = await get(url)
    return parse_cluster_url_output(body)