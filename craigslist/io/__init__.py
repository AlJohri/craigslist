import logging

logger = logging.getLogger(__name__)

def requests_get(url, timeout=10):
    logger.debug("downloading %s" % url)
    import requests
    return requests.get(url, timeout=timeout).text

async def asyncio_get(url, timeout=10):
    logger.debug("downloading %s" % url)
    import aiohttp
    import async_timeout
    async with aiohttp.ClientSession() as session:
        with async_timeout.timeout(timeout):
            async with session.get(url) as r:
                return await r.text()

# def asyncio_queue():
#     from asyncio import Queue
#     return Queue

# async def tornado_get():
#     from tornado import httpclient
#     # http_client = httpclient.AsyncHTTPClient(max_clients=CONCURRENCY)
#     # await http_client.fetch(url, connect_timeout=5, request_timeout=45)
#     pass

from craigslist.io.debug_executor import DebugExecutor
