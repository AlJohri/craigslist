import logging
from craigslist.search.jsonsearch import parse_cluster_url_output

logger = logging.getLogger(__name__)

async def jsonsearch():
    pass

async def process_cluster_url(url, get):
    logger.debug("downloading %s" % url)
    body = await get(url)
    return parse_cluster_url_output(body)