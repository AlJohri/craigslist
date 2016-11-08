class FakeCondition:
    def __init__(self):
        self.acquire = lambda: None
        self.release = lambda: None

    def __enter__(self):
        pass

    def __exit__(self, *args):
        pass

class FakeFuture:
    def __init__(self, fn, *args, **kwargs):
        self.fn = fn
        self.args = args
        self.kwargs = kwargs
        self._condition = FakeCondition()
        self._state = 'FINISHED'
        self._waiters = []

    def result(self):
        return self.fn(*self.args, **self.kwargs)

class FakeExecutor:

    def __init__(self, max_workers=None):
        pass

    def submit(self, fn, *args, **kwargs):
        return FakeFuture(fn, *args, **kwargs)

def requests_get(url):
    import requests
    return requests.get(url).text

async def asyncio_get():
    import aiohttp
    async with aiohttp.get(url) as r:
        return await r.text()

async def tornado_get():
    from tornado import httpclient
    # http_client = httpclient.AsyncHTTPClient(max_clients=CONCURRENCY)
    # await http_client.fetch(url, connect_timeout=5, request_timeout=45)
    pass