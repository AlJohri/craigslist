def requests_get(url):
    import requests
    return requests.get(url).text

async def asyncio_get(url):
    import aiohttp
    async with aiohttp.get(url) as r:
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
